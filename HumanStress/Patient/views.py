from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

from sklearn.svm import SVC
import pandas as pd
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer


from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from .models import HumanStress
# Create your views here.

"""def placement(request):
    return render(request,"placement.html")"""

def register(request):
    if request.method == 'POST':
        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        c_password=request.POST.get('c_password')

        if password == c_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return render(request,'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return render(request,'register.html')
            else:
                #save data in db
                user = User.objects.create_user(first_name=firstName, last_name=lastName, email=email,username=username,password=password)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request,'register.html')
            return redirect('/')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user =auth.authenticate(username=username, password=password)

        if user is not None:
            print('Authenticated')
            return redirect('stress')
        else:
            print('Not authenticated')
            messages.info(request, 'Invalid credentials')
            return render(request,'login.html')
    else:
        return render(request, 'login.html')

def predict(request):
    if request.method=="POST":
        sr=float(request.POST['sr'])
        rr=float(request.POST['rr'])
        t=float(request.POST['t'])
        lm=float(request.POST['lm'])
        bo=float(request.POST['bo'])
        rem=float(request.POST['rem'])
        sr1=float(request.POST['sr1'])
        hr=float(request.POST['hr'])
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import warnings
        warnings.filterwarnings('ignore')

        data = pd.read_csv(r'static/Datasets/SaYoPillow.csv')
        print(data.info())
        data.rename(columns={'sr': 'snoring rate', 'rr':'respiration rate', 't': 'body temperature', 'lm':'limb movement',
                            'bo':'blood oxygen', 'rem':'eye movement', 'sr.1':'sleeping hours', 'hr':'heart rate',
                            'sl':'stress level'}, inplace=True)
        print(data.columns)
        print(data.describe())
        sns.set(style="whitegrid")
        sns.countplot(x='stress level', data=data)
        plt.show()
        from mlxtend.preprocessing import minmax_scaling

        X = data.drop('stress level', axis=1)
        y = pd.DataFrame(data['stress level'])

        X_scaled = minmax_scaling(X, columns=X.columns)
        from sklearn.feature_selection import mutual_info_regression

        mi = pd.DataFrame(mutual_info_regression(X_scaled, y), columns=['MI Scores'], index=X_scaled.columns)
        corr = pd.DataFrame(X_scaled[X_scaled.columns].corrwith(y['stress level']), columns=['Correlation'])
        s_corr = pd.DataFrame(X_scaled[X_scaled.columns].corrwith(y['stress level'], method='spearman'),
                            columns=['Spearman_Correlation'])

        relation = mi.join(corr)
        relation = relation.join(s_corr)
        relation.sort_values(by='MI Scores', ascending=False)
        from sklearn.model_selection import train_test_split

        X_train, X_valid, y_train, y_valid = train_test_split(X_scaled, y, train_size=0.8, test_size=0.2, random_state=42,
                                                            stratify = y, shuffle=True)
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.naive_bayes import GaussianNB
        from sklearn.svm import LinearSVC
        from sklearn.svm import SVC
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.linear_model import SGDClassifier
        from sklearn.ensemble import GradientBoostingClassifier

        from sklearn.metrics import accuracy_score

        dtc = DecisionTreeClassifier()
        lr = LogisticRegression()
        gnb = GaussianNB()
        lsvc = LinearSVC()
        svc = SVC()
        rfc = RandomForestClassifier()
        knn = KNeighborsClassifier()
        sgdc = SGDClassifier()
        gbc = GradientBoostingClassifier()

        models = [dtc, lr, gnb, lsvc, svc, rfc,  knn, sgdc, gbc]
        model_name = ['Decision Tree', 'Logistic Regression', 'Gaussian Naive Bayes', 'Linear SVC', 'SVC', 'Random Forest',
                    'KNN or k-Nearest Neighbors', 'Stochastic Gradient Descent', 'Gradient Boosting']

        acc_scores = []
        for model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_valid)
            acc_model = round(accuracy_score(y_pred, y_valid) * 100, 2)
            acc_scores.append(acc_model)
        models_acc = pd.DataFrame({'Model name': model_name, 'Accuracy scores': acc_scores})
        models_acc.sort_values(by='Accuracy scores', ascending=False)
        from sklearn.model_selection import RepeatedStratifiedKFold
        from sklearn.model_selection import cross_val_score

        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3)
        cv_mean_scores = []
        for model in models:
            scores = cross_val_score(model, X_scaled, y, cv=cv, scoring='accuracy')
            cv_mean_scores.append(scores.mean()*100)
        models_val = pd.DataFrame({'Model name': model_name, 'Cross validation mean scores': cv_mean_scores})
        models_val.sort_values(by='Cross validation mean scores', ascending=False)
        from sklearn.metrics import precision_score, recall_score, f1_score

        y_pred = lr.predict(X_valid)

        print('Precision score is: {:2f} \nRecall score is: {:2f} \nf1 score is: {:2f}'.format(
            precision_score(y_valid, y_pred, average='weighted'),
            recall_score(y_valid, y_pred, average='weighted'),
            f1_score(y_valid, y_pred, average='weighted')))
        from sklearn.metrics import classification_report

        report_svc = pd.DataFrame(classification_report(y_valid, y_pred, output_dict=True))
        print(report_svc)
        from sklearn.metrics import confusion_matrix

        cm = confusion_matrix(y_valid, y_pred)

        cm_dataframe = pd.DataFrame(cm, columns=lr.classes_, index=lr.classes_)
        plt.figure(figsize = (12,6));
        p = sns.heatmap(cm_dataframe, annot=True, fmt="d", annot_kws={"fontsize":15});
        p.set_title('Confusion Matrix', fontsize=20);
        p.set_xlabel('Predicted Classes');
        p.set_ylabel('Actual Classes');
        plt.show()
        import numpy as np
        pred_data=np.array([[sr,rr,lm,rem,t,bo,sr1,hr]],dtype=object)
        tree=DecisionTreeClassifier()
        tree.fit(X_train,y_train)
        prediction=tree.predict(pred_data)
        humanstress=HumanStress.objects.create(snoring_rate=sr,respiration_rate=rr,
        body_temperature=t,blood_oxygen=bo,eye_movement=rem,
        sleeping_hours=sr1,heart_rate=hr,limb_movement=lm,stress_level=prediction)
        humanstress.save()
        return render(request,"predict.html",{
                "sr":sr,"rr":rr,"t":t,"lm":lm,"rem":rem,"bo":bo,"sr1":sr1,"hr":hr,"prediction":prediction
        })
    return render(request,"predict.html")

def stress(request):
    return render(request,"stress.html")

def logout(request):
    auth.logout(request)
    return render(request,"login.html")

def home(request):
    return render(request,"index.html")

def logout(request):
    auth.logout(request)
    return redirect('/')



        

