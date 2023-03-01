from flask import Flask,request,render_template, redirect
from neo4j import GraphDatabase
import csv

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()
    def query(self, query, db=None, parameter=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            if parameter == None:
                response = list(session.run(query))
            else:
                response = list(session.run(query, parameter))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

with open("cred.txt")as f1:
 data=csv.reader(f1,delimiter=",")
 for row in data:
    id=row[0]
    pwd=row[1]
 f1.close()

conn = Neo4jConnection(uri="bolt://localhost:7687", user=id, password=pwd)



app=Flask(__name__)
@app.route("/graph",methods=["GET","POST"])
def creategrpah():
    if request.method=="POST":
        if request.form["submit"]=="find_graph":
         
         query_string="""
         MATCH(a:Person)
         return a.name as name ,a.event_id as event_id
         """
         results=conn.query(query_string, db='graphDb')

         graphs=[]
         for result in results:
            dc={}
            name=result["name"]
            event_id=result["event_id"]
            dc.update({"Name":name,"Event_id":event_id})
            graphs.append(dc)

         print(graphs)
         return render_template("results.html",list=graphs)

        elif request.form["submit"]=="find_property":
             name=request.form["name"]
             query_string="""
             MATCH(a:Person{name:$name})
             return a.name as name ,a.event_id as event_id
             """  
             parameter={"name":name}
             results=conn.query(query_string, db='graphDb', parameter=parameter)
             for result in results:
                name=result["name"]
                event_id=result["event_id"]

             return (f"{name} has event id {event_id}")

        elif request.form["submit"]=="find_friends":
             name_requested=request.form["friends"]
             query_string="""
             match(a:Person{name:$name})
             with [(a)--(b)|b.name]as names
             unwind names as name
             return name
             """  
             parameter={"name":name_requested}
             results=conn.query(query_string,db='graphDb', parameter=parameter)
             friends=[]
             for result in results:
                name=result["name"]
                friends.append(name)
                
             if(len(friends)>0):
                 return render_template("friends.html",list=friends,name=name_requested)
             else:
                 return("no friends or invalid person")

        
    else:
        return render_template("index.html")


if __name__ == '__main__':

    app.run(port=5000)
