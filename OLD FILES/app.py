from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, user_logged_in
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask import Flask, redirect, render_template, request, url_for
from Pas import Password
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import math

#flask
app = Flask(__name__)

#Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User_DATA.sqlite'
app.config['SECRET_KEY'] = Password 
bcrypt = Bcrypt(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

#More Login stuff
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('base2'))

    return render_template('login.html', form = form)

# NON-Page routes
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user
    return redirect(url_for('hello'))

#Program files 
@app.route('/darkmode')
def darkmode():
    return redirect(url_for('base2d'))

@app.route('/Register/', methods = ['GET', 'POST'])
def register(): 
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form = form)

@app.route('/base2/', methods = ['GET', 'POST'])
@login_required
def base2():
    return render_template('base2.html')

@app.route('/base2d/', methods = ['GET', 'POST'])
@login_required
def base2d():
    return render_template('base2.html')

@app.route('/Documentation', methods = ['GET', 'POST'])
def Documentation():
    return render_template('Documentation.html')

@app.route('/Memberships', methods = ['POST', 'GET'])
def Memberships():
    return render_template('Membership.html')

@app.route('/')
def hello():
    return render_template('Home.html')

@app.route('/Program/', methods = ['GET', 'POST'])
@login_required
def program():
    error1 = None
    if request.method == 'POST':

        if request.form['function'] == "temp":
            return redirect(url_for('temp')) 
        
        if request.form['function'] == "re":
            return redirect(url_for('re')) 

        if request.form['function'] == "qf":
            return redirect(url_for('qf'))
        
        if request.form['function'] == "qfx":
            return redirect(url_for('qf2'))

        if request.form['function'] == "tr":
            return redirect(url_for('trithingys'))
        
        if request.form['function'] == "pa":
            return redirect(url_for('Pa'))

        else: 
            error1 = 'Invalid value Entered'
    return render_template('program.html', error=error1)

#Trythingys redirector
@app.route('/trithingys/', methods= ['GET', 'POST'])
@login_required
def trithingys():
    if request.method == 'POST':
        if request.form['function'] == 'ro':
            return redirect(url_for('ro'))

        if request.form['function'] == 'q':
            return redirect(url_for('Q'))

        if request.form['function'] == 'ec':
            return redirect(url_for('EC'))
        
        if request.form['function'] == 'v':
            return redirect(url_for('V'))
        
        if request.form['function'] == 'v2':
            return redirect(url_for('V2'))

        if request.form['function'] == 'f':
            return redirect(url_for('forces'))
        
        if request.form['function'] == 'a':
            return redirect(url_for('acceleration'))

        if request.form['function'] == 'wl':
            return redirect(url_for('lamda'))

    return render_template('trithingys.html')

# Conversion Program files
@app.route('/Conversions/', methods=['GET', 'POST'])
@login_required
def Conversions():
    if request.method == 'POST':
        if request.form['function'] == "len":
            return redirect(url_for('len'))
        
        if request.form['function'] == "mass":
            return redirect(url_for('mass'))
        
        if request.form['function'] == "time":
            return redirect(url_for('time'))

        if request.form['function'] == "temp":
            return redirect(url_for('temp')) 
        
        if request.form['function'] == "lq":
            return redirect(url_for('liquids'))  

        global base2
        
        if user_logged_in:
            base2 = True
       
        else: 
            base2 = False

    return render_template('Conversions.html', base2 = base2)

# Conversion Program files
@app.route('/Conversions_Login/', methods=['GET', 'POST'])
@login_required
def Conversions_Login():
    if request.method == 'POST':
        if request.form['function'] == "len":
            return redirect(url_for('len_Login'))
        
        if request.form['function'] == "mass":
            return redirect(url_for('mass_Login'))
        
        if request.form['function'] == "time":
            return redirect(url_for('time_Login'))

        if request.form['function'] == "temp":
            return redirect(url_for('temp_Login')) 
        
        if request.form['function'] == "lq":
            return redirect(url_for('liquids_Login'))  

    return render_template('Conversions_login.html')

@app.route('/DISCLAMER/')
def DISCLAMER():
    return render_template('disclamer.html')

@app.route('/DISCLAMERLoged/')
def DISCLAMERLoged():
    return render_template('disclamer_logedin.html')

@app.route('/Users/')
@login_required
def Users():
    return render_template('Users.html')
  

# program files 

@app.route('/len/', methods = ['GET', 'POST'])
@login_required
def len(): 
    if request.method == "POST":
        
        num = request.form['len']

        mkm : float = float(num) / 1000
        mcm : float = float(num) * 100
        mft : float = float(num) * 3.28 
        myd : float = float(num) * 1.094
        mmi : float = float(num) / 1809
        mmm : float = float(num) * 1000
        mμm : float = float(num) * 1e+6
        mnm : float = float(num) * 1e+9
        m_in : float = float(num) * 39.37

        kmin : float = float(num) * 39370
        kmm : float = float(num) * 1000
        kmcm : float = float(num) * 100000
        kmft : float = float(num) * 3281
        kmyd : float = float(num) * 1094
        kmmi : float = float(num) / 1.609
        kmmm : float = float(num) * 1e+6
        kmμm : float = float(num) * 1e+9
        kmnm : float = float(num) * 1e+12
        kmin : float = float(num) * 39370
    
        cmm : float = (float(num) / 100)
        cmkm : float = (float(num) / 100_000)
        cmft : float = (float(num) / 30.48)
        cmyd : float = (float(num) / 41.44)
        cmmi : float = (float(num) / 160934)
        cmmm : float = float(num) * 10
        cmμm : float = float(num) * 1e+4
        cmnm : float = float(num) * 1e+7
        cmin : float = float(num) / 2.54

        ftm : float = (float(num) * 3.281)
        ftkm : float = (float(num) / 3281)
        ftcm : float = (float(num) / 30.48)
        ftyd : float = (float(num) * 3)
        ftmi : float = (float(num) / 5280)
        ftmm : float = float(num) * 304.8
        ftμm : float = float(num) * 304800
        ftnm : float = float(num) * 3.048e+8
        ftin : float = float(num) * 12
        
        ydm : float = (float(num) * 1.094)
        ydkm : float = (float(num) / 1094)
        ydcm : float = (float(num) * 91.44)
        ydft : float = (float(num) / 3)
        ydmi : float = (float(num) /1760)
        ydmm : float = float(num) * 914.4
        ydμm : float = float(num) * 914400
        ydnm : float = float(num) * 9.144e+8
        ydin : float = float(num) / 12
            
        mim : float = (float(num) * 1609)
        mikm : float = (float(num) * 1.609)
        micm : float = (float(num) * 160934)
        mift : float = (float(num) * 5280)
        miyd : float = (float(num) * 1760 )
        mimm : float = float(num) * 1.609e+6
        miμm : float = float(num) * 1.609e+9
        minm : float = float(num) * 1.609e+12
        miin : float = float(num) * 63360

        mm_m : float = float(num) / 1000
        mmkm : float = float(num) / 1e+6
        mmcm : float = float(num) / 10
        mmft : float = float(num) / 304.8
        mmyd : float = float(num) / 914.4
        mmim : float = float(num) / 1.609e+6
        mmμm : float = float(num) * 1000
        mmnm : float = float(num) * 1e+6
  
        μmm : float = float(num) / 1e+6
        μmkm : float = float(num) / 1e+9
        μmcm : float = float(num) / 1e+4
        μmft : float = float(num) / 304800
        μmyd : float = float(num) / 914400
        μmmi : float = float(num) / 1.609e+9
        μmmm : float = float(num) / 1000
        μmnm : float = float(num) * 1000
        μmin : float = float(num) / 25400




        if request.form['submit2'] == 'Enter': 
            return render_template( 'len.html', 
            mkm = mkm, mcm = mcm, mft = mft, myd = myd, mmi = mmi, min = m_in, 
            kmm = kmm, kmcm = kmcm, kmft = kmft, kmyd = kmyd, kmmi = kmmi, kmin = kmin, 
            cmm = cmm, cmkm = cmkm, cmft = cmft, cmyd = cmyd, cmmi = cmmi, cmin = cmin, 
            ftm = ftm, ftkm = ftkm, ftcm = ftcm, ftyd = ftyd, ftmi= ftmi, ftin= ftin, 
            ydm = ydm, ydkm = ydkm, ydcm = ydcm, ydft = ydft, ydmi = ydmi, ydin = ydin, 
            mim = mim, mikm = mikm, micm = micm, mfit = mift, miyd =miyd, miin = miin,
            mmm = mm_m, mmkm = mmkm, mmcm = mmcm, mmft = mmft, mmyd = mmyd, mmmi = mmim, mmμm = mmμm, mmnm = mmnm, 
            μmm = μmm, μmkm = μmkm, μmcm = μmcm, μmft = μmft, μmyd = μmyd,
            num=num) 

    return render_template('len.html',)

@app.route('/len_Login/', methods = ['GET', 'POST'])
@login_required
def len_Login(): 
    if request.method == "POST":
        
        num = request.form['len']

        mkm : float = float(num) / 1000
        mcm : float = float(num) * 100
        mft : float = float(num) * 3.28 
        myd : float = float(num) * 1.094
        mmi : float = float(num) / 1809
        mmm : float = float(num) * 1000
        mμm : float = float(num) * 1e+6
        mnm : float = float(num) * 1e+9
        m_in : float = float(num) * 39.37

        kmin : float = float(num) * 39370
        kmm : float = float(num) * 1000
        kmcm : float = float(num) * 100000
        kmft : float = float(num) * 3281
        kmyd : float = float(num) * 1094
        kmmi : float = float(num) / 1.609
        kmmm : float = float(num) * 1e+6
        kmμm : float = float(num) * 1e+9
        kmnm : float = float(num) * 1e+12
        kmin : float = float(num) * 39370
    
        cmm : float = (float(num) / 100)
        cmkm : float = (float(num) / 100_000)
        cmft : float = (float(num) / 30.48)
        cmyd : float = (float(num) / 41.44)
        cmmi : float = (float(num) / 160934)
        cmmm : float = float(num) * 10
        cmμm : float = float(num) * 1e+4
        cmnm : float = float(num) * 1e+7
        cmin : float = float(num) / 2.54

        ftm : float = (float(num) * 3.281)
        ftkm : float = (float(num) / 3281)
        ftcm : float = (float(num) / 30.48)
        ftyd : float = (float(num) * 3)
        ftmi : float = (float(num) / 5280)
        ftmm : float = float(num) * 304.8
        ftμm : float = float(num) * 304800
        ftnm : float = float(num) * 3.048e+8
        ftin : float = float(num) * 12
        
        ydm : float = (float(num) * 1.094)
        ydkm : float = (float(num) / 1094)
        ydcm : float = (float(num) * 91.44)
        ydft : float = (float(num) * 3)
        ydmi : float = (float(num) /1760)
        ydmm : float = float(num) * 914.4
        ydμm : float = float(num) * 914400
        ydnm : float = float(num) * 9.144e+8
        ydin : float = float(num) * 36
            
        mim : float = (float(num) * 1609)
        mikm : float = (float(num) * 1.609)
        micm : float = (float(num) * 160934)
        mift : float = (float(num) * 5280)
        miyd : float = (float(num) * 1760 )
        mimm : float = float(num) * 1.609e+6
        miμm : float = float(num) * 1.609e+9
        minm : float = float(num) * 1.609e+12
        miin : float = float(num) * 63360

        mm_m : float = float(num) / 1000
        mmkm : float = float(num) / 1e+6
        mmcm : float = float(num) / 10
        mmft : float = float(num) / 304.8
        mmyd : float = float(num) / 914.4
        mmim : float = float(num) / 1.609e+6
        mmμm : float = float(num) * 1000
        mmnm : float = float(num) * 1e+6
  
               

        if request.form['submit2'] == 'Enter': 
            return render_template( 'len_login.html', 
            mkm = mkm, mcm = mcm, mft = mft, myd = myd, mmi = mmi, min = m_in, 
            kmm = kmm, kmcm = kmcm, kmft = kmft, kmyd = kmyd, kmmi = kmmi, kmin = kmin, 
            cmm = cmm, cmkm = cmkm, cmft = cmft, cmyd = cmyd, cmmi = cmmi, cmin = cmin, 
            ftm = ftm, ftkm = ftkm, ftcm = ftcm, ftyd = ftyd, ftmi= ftmi, ftin= ftin, 
            ydm = ydm, ydkm = ydkm, ydcm = ydcm, ydft = ydft, ydmi = ydmi, ydin = ydin, 
            mim = mim, mikm = mikm, micm = micm, mfit = mift, miyd =miyd, miin = miin,
            num=num) 

    return render_template('len_login.html',)

@app.route('/mass/', methods = ['GET', 'POST'])
@login_required
def mass():

    if request.method == 'POST':
        kgg : float = (float(request.form['num']) * 1000)
        kgton : float = (float(request.form['num']) / 907)
        kglbs : float = (float(request.form['num']) * 2.205)
        kgmg : float = (float(request.form['num']) / 100_000_0)
            

        gkg : float = (float(request.form['num']) / 1000)
        gton : float = (float(request.form['num']) / 907185)
        glbs : float = (float(request.form['num']) / 454)
        gmg : float = (float(request.form['num']) * 1000)
            
        mgkg : float = (float(request.form['num']) / 100_000_0)
        mgg : float = (float(request.form['num']) / 1000)
        mgton : float = (float(request.form['num']) / 100_000_000_0)
        mglbs : float = (float(request.form['num']) / 1453592)
            

        tonkg : float = (float(request.form['num']) * 907)
        tong : float = (float(request.form['num']) * 907195)
        tonlbs : float = (float(request.form['num']) * 2000)
        tonmg : float = (float(request.form['num']) * 100_000_000_0)


        lbskg : float = (float(request.form['num']) / 2.205)
        lbsg : float = (float(request.form['num']) *454)
        lbston : float = (float(request.form['num']) / 2000)
        lbsmg : float = (float(request.form['num']) / 453_592 )

        if request.form['submit'] == 'Enter': 
            return render_template( 'mass.html',kgg =kgg, kgton = kgton, kglbs = kglbs, kgmg = kgmg, 
            gkg = gkg, gton =gton, glbs = glbs, gmg = gmg,
            mgkg = mgkg, mgg = mgg, mgton = mgton, mglbs = mglbs,
            tonkg = tonkg, tong = tong, tonlbs = tonlbs, tonmg = tonmg, 
            lbskg = lbskg, lbsg = lbsg, lbston = lbston, lbsmg = lbsmg ) 

    return render_template('mass.html',)

@app.route('/mass_Login/', methods = ['GET', 'POST'])
@login_required
def mass_Login():

    if request.method == 'POST':
        kgg : float = (float(request.form['num']) * 1000)
        kgton : float = (float(request.form['num']) / 907)
        kglbs : float = (float(request.form['num']) * 2.205)
        kgmg : float = (float(request.form['num']) / 100_000_0)
            

        gkg : float = (float(request.form['num']) / 1000)
        gton : float = (float(request.form['num']) / 907185)
        glbs : float = (float(request.form['num']) / 454)
        gmg : float = (float(request.form['num']) * 1000)
            
        mgkg : float = (float(request.form['num']) / 100_000_0)
        mgg : float = (float(request.form['num']) / 1000)
        mgton : float = (float(request.form['num']) / 100_000_000_0)
        mglbs : float = (float(request.form['num']) / 1453592)
            

        tonkg : float = (float(request.form['num']) * 907)
        tong : float = (float(request.form['num']) * 907195)
        tonlbs : float = (float(request.form['num']) * 2000)
        tonmg : float = (float(request.form['num']) * 100_000_000_0)


        lbskg : float = (float(request.form['num']) / 2.205)
        lbsg : float = (float(request.form['num']) *454)
        lbston : float = (float(request.form['num']) / 2000)
        lbsmg : float = (float(request.form['num']) / 453_592 )

        if request.form['submit'] == 'Enter': 
            return render_template( 'mass_login.html',kgg =kgg, kgton = kgton, kglbs = kglbs, kgmg = kgmg, 
            gkg = gkg, gton =gton, glbs = glbs, gmg = gmg,
            mgkg = mgkg, mgg = mgg, mgton = mgton, mglbs = mglbs,
            tonkg = tonkg, tong = tong, tonlbs = tonlbs, tonmg = tonmg, 
            lbskg = lbskg, lbsg = lbsg, lbston = lbston, lbsmg = lbsmg ) 

    return render_template('mass_login.html',)

@app.route('/time/', methods = ['GET', 'POST'])
@login_required
def time(): 
    if request.method == 'POST':
        sm : float = (float(request.form['num']) / 60)
        sh : float = (float(request.form['num']) / 3600)

        ms : float = (float(request.form['num']) * 60)
        mh : float = (float(request.form['num']) / 60) 

        hs : float = (float(request.form['num']) * 60)
        hm : float = (float(request.form['num']) * 3600)

        if request.form['submit'] == 'Enter': 
            return render_template('time.html', sm = sm, sh = sh, ms = ms, mh = mh, hs = hs, hm = hm )
    
    return render_template('time.html')

@app.route('/time_Login/', methods = ['GET', 'POST'])
@login_required
def time_Login(): 
    if request.method == 'POST':
        sm : float = (float(request.form['num']) / 60)
        sh : float = (float(request.form['num']) / 3600)

        ms : float = (float(request.form['num']) * 60)
        mh : float = (float(request.form['num']) / 60) 

        hs : float = (float(request.form['num']) * 60)
        hm : float = (float(request.form['num']) * 3600)

        if request.form['submit'] == 'Enter': 
            return render_template('time_login.html', sm = sm, sh = sh, ms = ms, mh = mh, hs = hs, hm = hm )
    
    return render_template('time_login.html')


@app.route('/temp/', methods = ['GET', 'POST'])
@login_required
def temp():
    if request.method == 'POST': 
        kc : float = (float(request.form['num']) - 273.15)
        kf : float = ((float(request.form['num']) - 273.15) * 9/5 + 32)
    
        ck: float = (float(request.form['num']) + 273.15)
        cf : float = ((float(request.form['num']) * 9/5) + 32)

        fk : float = ((float(request.form['num']) - 32) * 5/9 + 273.15)
        fc : float = ((float(request.form['num']) - 32) * 5/9)
                
        if request.form['submit'] == 'Enter':
            return render_template('temp.html', kc=kc, kf=kf, ck=ck, cf=cf, fk=fk, fc=fc)

    return render_template('temp.html')

@app.route('/temp_Login/', methods = ['GET', 'POST'])
@login_required
def temp_Login():
    if request.method == 'POST': 
        kc : float = (float(request.form['num']) - 273.15)
        kf : float = ((float(request.form['num']) - 273.15) * 9/5 + 32)
    
        ck: float = (float(request.form['num']) + 273.15)
        cf : float = ((float(request.form['num']) * 9/5) + 32)

        fk : float = ((float(request.form['num']) - 32) * 5/9 + 273.15)
        fc : float = ((float(request.form['num']) - 32) * 5/9)
                
        if request.form['submit'] == 'Enter':
            return render_template('temp_login.html', kc=kc, kf=kf, ck=ck, cf=cf, fk=fk, fc=fc)

    return render_template('temp_login.html')


@app.route('/Liquids/', methods = ['GET', 'POST'])
@login_required
def liquids(): 
    if request.method == 'POST': 
        lcl : float = float(request.form['num']) * 100
        lml : float = float(request.form['num']) * 1000
        loz : float = float(request.form['num']) * 32.1951

        cll : float = float(request.form['num']) / 100
        clml : float = float(request.form['num']) * 10
        cloz : float = float(request.form['num']) / 2.841

        mll : float = float(request.form['num']) / 1000
        mlcl : float = float(request.form['num']) / 10
        mloz : float = float(request.form['num']) / 28.413

        ozl : float = float(request.form['num']) / 35.195
        ozcl : float = float(request.form['num']) * 2.841
        ozml : float = float(request.form['num']) * 28.413
 
        if request.form['submit'] == 'Enter': 
            return render_template('liquids.html', lcl = lcl, lml = lml, loz = loz, 
            cll = cll, clml = clml, cloz = cloz, mll = mll, mlcl = mlcl, mloz = mloz, 
            ozl = ozl, ozcl = ozcl, ozml = ozml)
    
    return render_template('liquids.html')

@app.route('/Liquids_Login/', methods = ['GET', 'POST'])
@login_required
def liquids_Login(): 
    if request.method == 'POST': 
        lcl : float = float(request.form['num']) * 100
        lml : float = float(request.form['num']) * 1000
        loz : float = float(request.form['num']) * 32.1951

        cll : float = float(request.form['num']) / 100
        clml : float = float(request.form['num']) * 10
        cloz : float = float(request.form['num']) / 2.841

        mll : float = float(request.form['num']) / 1000
        mlcl : float = float(request.form['num']) / 10
        mloz : float = float(request.form['num']) / 28.413

        ozl : float = float(request.form['num']) / 35.195
        ozcl : float = float(request.form['num']) * 2.841
        ozml : float = float(request.form['num']) * 28.413
 
        if request.form['submit'] == 'Enter': 
            return render_template('liquids_login.html', lcl = lcl, lml = lml, loz = loz, 
            cll = cll, clml = clml, cloz = cloz, mll = mll, mlcl = mlcl, mloz = mloz, 
            ozl = ozl, ozcl = ozcl, ozml = ozml)
    
    return render_template('liquids_login.html')
# Re files
 
@app.route('/re/', methods = ['GET', 'POST'])
@login_required
def re(): 
    if request.method == 'POST': 
        if request.form['Circuittype'] == 'sr': 
            return redirect(url_for('resr'))

        if request.form['Circuittype'] == 'pl': 
            return redirect(url_for('repl'))

    return render_template('re.html')

@app.route('/reseries/', methods = ['GET', 'POST'])
@login_required
def resr(): 
    if request.method == 'POST':
        if request.form['numRs'] == '2': 
            return redirect(url_for('re2sr'))
        
        if request.form['numRs'] == '3': 
            return redirect(url_for('re3sr'))

        if request.form['numRs'] == '4': 
            return redirect(url_for('re4sr'))

        if request.form['numRs'] == '5': 
            return redirect(url_for('re5sr'))
 
    return render_template('resr.html')

@app.route('/re2sr/', methods = ['GET', 'POST'])
@login_required
def re2sr(): 
    if request.method == 'POST': 
        re : float = float(request.form['r1']) + float(request.form['r2'])
    
        if request.form['submit'] == 'Enter': 
            return render_template('re2sr.html', re = re)
    return render_template('re2sr.html')


@app.route('/re3sr/', methods = ['GET', 'POST'])
@login_required
def re3sr(): 
    if request.method == 'POST': 
        re : float = float(request.form['r1']) + float(request.form['r2']) + float(request.form['r3'])
    
        if request.form['submit'] == 'Enter': 
            return render_template('re3sr.html', re = re)
    return render_template('re3sr.html')

@app.route('/re4sr/', methods = ['GET', 'POST'])
@login_required
def re4sr(): 
    if request.method == 'POST': 
        re : float = float(request.form['r1']) + float(request.form['r2']) + float(request.form['r3']) + float(request.form['r4'])
    
        if request.form['submit'] == 'Enter': 
            return render_template('re4sr.html', re = re)
    return render_template('re4sr.html')

@app.route('/re5sr/', methods = ['GET', 'POST'])
@login_required
def re5sr(): 
    if request.method == 'POST': 
        re : float =  float(request.form['r1']) + float(request.form['r2']) + float(request.form['r3']) + float(request.form['r4']) + float(request.form['r5'])
    
        if request.form['submit'] == 'Enter': 
            return render_template('re5sr.html', re = re)
    return render_template('re5sr.html')

@app.route('/reparallel/', methods = ['GET', 'POST'])
@login_required
def repl(): 
    if request.method == 'POST':
        if request.form['numR'] == '2': 
            return redirect(url_for('re2pl'))
        
        if request.form['numR'] == '3': 
            return redirect(url_for('re3pl'))

        if request.form['numR'] == '4': 
            return redirect(url_for('re4pl'))

        if request.form['numR'] == '5': 
            return redirect(url_for('re5pl'))

    return render_template('repl.html')

@app.route('/re2pl/', methods = ['GET', 'POST'])
@login_required
def re2pl(): 
    if request.method == 'POST': 
        re : float = (1 / float(request.form['r1']) + 1 / float(request.form['r2'])) ** -1
    
        if request.form['submit'] == 'Enter': 
            return render_template('re2pl.html', re = re)
    return render_template('re2pl.html')

@app.route('/re3pl/', methods = ['GET', 'POST'])
@login_required
def re3pl(): 
    if request.method == 'POST': 
        re : float = (1 / float(request.form['r1']) + 1 / float(request.form['r2']) + 1 / float(request.form['r3']) ) ** -1
    
        if request.form['submit'] == 'Enter': 
            return render_template('re3pl.html', re = re)
    return render_template('re3pl.html')

@app.route('/re4pl/', methods = ['GET', 'POST'])
@login_required
def re4pl(): 
    if request.method == 'POST': 
        re : float = (1 / float(request.form['r1']) + 1 / float(request.form['r2']) + 1 / float(request.form['r3']) + 1 / float(request.form['r4']) ) ** -1
    
        if request.form['submit'] == 'Enter': 
            return render_template('re4pl.html', re = re)
    return render_template('re4pl.html')

@app.route('/re5pl/', methods = ['GET', 'POST'])
@login_required
def re5pl(): 
    if request.method == 'POST': 
        re : float = (1 / float(request.form['r1']) + 1 / float(request.form['r2']) + 1 / float(request.form['r3']) + 1 / float(request.form['r4']) + 1 / float(request.form['r5'])) ** -1
    
        if request.form['submit'] == 'Enter': 
            return render_template('re5pl.html', re = re)
    return render_template('re5pl.html')

@app.route('/qf/', methods = ['GET', 'POST'])
@login_required
def qf():
    if request.method == 'POST':
        x : float = (-1 * float(request.form['b'])) / (float(request.form['a']) * 2)
        x2 : float = float(x) * float(x)
        a : float = float(request.form['a']) * float(x2) 
        b : float = float(request.form['b']) * float(x)
        y : float = float(a) + float(b) + float(request.form['c'])

        if request.form['submit'] == 'Enter':   
            return render_template('qf.html', y1 = y, x1 = x)

    return render_template('qf.html')

@app.route('/qf2/', methods = ['GET', 'POST'])
@login_required
def qf2(): 
    if request.method == 'POST': 

        if request.form['submit'] == 'Enter Y Values': 
            x : float = (-1 * float(request.form['b'])) / (float(request.form['a']) * 2)
            x2 : float = float(x) * float(x)
            a : float = float(request.form['a']) * float(x2) 
            b : float = float(request.form['b']) * float(x)
            y : float = float(a) + float(b) + float(request.form['c'])
            return render_template('qf2.html', y =y, x=x)

        if request.form['submit'] == 'Enter X Values':
            def nor_y( x: float = request.form['x1'], a: float = request.form['a'], b: float = request.form['b'], c: float = request.form['c']):
                x1 = x
                x2 : float = float(x) * float(x)
                a1 : float = float(a) * float(x2) 
                b1 : float = float(b) * float(x)
                y1 : float = float(a1) + float(b1) + float(c)
                return y1
            
            def nor_x(x: float = request.form['x1']): 
                x1 = x
                return x1

            y1 = nor_y()
            x1 = nor_x()

            y2 = nor_y(x = request.form['x2'])
            x2_ = nor_x(x = request.form['x2'])
        
            y3 = nor_y(x = request.form['x3'])
            x3 = nor_x(x = request.form['x3'])

            return render_template('qf2.html', y1 = y1, x1 = x1, y2 = y2, x2 = x2_, y3=y3, x3=x3)

    return render_template('qf2.html')

@app.route('/ro/', methods = ['GET', 'POST'])
@login_required
def ro():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v


        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('RO.html', m = mass, v = volume, ro = Density)
         
    return render_template('RO.html')

@app.route('/charge/', methods = ['GET', 'POST'])
@login_required
def Q():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('Q.html', m = mass, v = volume, ro = Density)
         
    return render_template('Q.html')

@app.route('/ec/', methods = ['GET', 'POST'])
@login_required
def EC():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('ec.html', m = mass, v = volume, ro = Density)
         
    return render_template('ec.html')

@app.route('/voltage/', methods = ['GET', 'POST'])
@login_required
def V():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('V.html', m = mass, v = volume, ro = Density)
         
    return render_template('V.html')
    
@app.route('/voltagesquared/', methods = ['GET', 'POST'])
@login_required
def V2():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        V : float = float(ro) * float(v)
        V2 : float = math.sqrt(V)
        Density : float = (float(m)**2) / float(v)
        volume : float = (float(m)**2) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('V2.html', m = V2, v = volume, ro = Density)
         
    return render_template('V2.html')

@app.route('/forces/', methods = ['GET', 'POST'])
@login_required
def forces():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('forces.html', m = mass, v = volume, ro = Density)
         
    return render_template('forces.html')

@app.route('/acceleration/', methods = ['GET', 'POST'])
@login_required
def acceleration():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('acceleration.html', m = mass, v = volume, ro = Density)
         
    return render_template('acceleration.html')

@app.route('/lamda/', methods = ['GET', 'POST'])
@login_required
def lamda():
    if request.method == 'POST': 
        
        ro = request.form['ro']
        v = request.form['v']
        m = request.form['m']

        if float(ro) == 0:
            ro = 1
        
        if float(v) == 0:
            v = 1

        if float(ro) == 0 or float(v) == 0: 
            mass = m

        if float(v) == 0 or float(m) == 0: 
            Density = ro

        if float(m) == 0 or float(ro) == 0: 
            volume = v

        mass : float = float(ro) * float(v)
        Density : float = float(m) / float(v)
        volume : float = float(m) / float(ro)

        if request.form['submit'] == 'Enter': 
            return render_template('lamda.html', m = mass, v = volume, ro = Density)
         
    return render_template('lamda.html')

@app.route('/Pascals/', methods = ['GET', 'POST'])
@login_required
def Pa():
    if request.method == 'POST':
        f1 = request.form['f1']
        f2 = request.form['f2']
        a1 = request.form['a1']
        a2 = request.form['a2']

        if float(f1) == 0 or f1 == '':
            f1 = 1
            f11 = float(a1) * float(f2)
            f1_out = float(f11) / float(a2)

        else:
            f1_out = f1

        if float(f2) == 0 or f2 == '':
            f2 = 1
            f21 = float(f1) * float(a2) 
            f2_out = float(f21) / float(a2)

        else:
            f2_out = f2

        if float(a1) == 0 or a1 == '':
            a1 = 1
            a11 = float(f1) * float(a2) 
            a1_out = float(a11) / float(f2)

        else:
            a1_out = a1

        if float(a2) == 0 or a2 == '':
            a2 = 1 
            a21 = float(a1) * float(f2) 
            a2_out = float(a21) / float(f1)

        else:
            a2_out = a2
    
        if request.form['submit'] == ' Calculate':
            return render_template('pa.html', f1= f1_out, f2 = f2_out, a1 = a1_out, a2 = a2_out)

    return render_template('pa.html')
