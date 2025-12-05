from flask import Flask, render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

#data class -row data
class MyTask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Integer,default=0)
    created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"Task{self.id}"

with app.app_context():
    db.create_all()
#routes for webpage

#homepage
@app.route("/",methods=["GET","POST"])
def index():

    #adding a task
    if request.method=="POST":
        current_task=request.form['content']
        new_task=MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            return f"Error:{e}"
        
    # see all current tasks
    else:
        tasks=MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)


# deleting a task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e: 
        return f"Error:{e}"


# edit a task
@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id:int):
    edit_task=MyTask.query.get_or_404(id)
    if request.method=="POST":
        edit_task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template("edit.html",task=edit_task)


#runner and debugger
if __name__ == "__main__":

    app.run(debug=True)