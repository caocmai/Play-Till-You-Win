import random
from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
# random.seed(40)

client = MongoClient()
db = client.first_intensive
tickets = db.tickets

app = Flask(__name__)
winning_nums = [2,3,6]

@app.route("/get_form_data", methods=["POST"])
def get_form_data():
  # num1 = request.form.get("number1")
  ticket = {
    "number1" : request.form.get("number1"),
    "number2" : request.form.get("number2"),
    "number3" : request.form.get("number3")
  }
  tickets.insert_one(ticket)
  # guessed_nums.append(int(num1))
  return redirect(url_for("view_ticket2"))

@app.route("/")
def index(): 
  return render_template("home.html", title={})

# Delete entire ticket list
@app.route("/delete_all")
def delete_all():
    tickets.remove()
    return redirect(url_for("index"))

@app.route("/view_ticket2")
def view_ticket2():
  return render_template("ticket_page2.html", tickets=tickets.find(), title="Check Ticket")

@app.route("/tickets/<ticket_id>/edit")
def edit_ticket(ticket_id):
  ticket = tickets.find_one({"_id": ObjectId(ticket_id)})
  return render_template("edit_ticket.html", ticket=ticket, title="Edit Ticket")

@app.route("/tickets/<ticket_id>", methods=["POST"])
def update_ticket(ticket_id):
  updated_ticket = {
    "number1" : request.form.get("number1"),
    "number2" : request.form.get("number2"),
    "number3" : request.form.get("number3")
  }
  tickets.update_one(
    {"_id": ObjectId(ticket_id)},
    {"$set": updated_ticket}
    )
  return render_template("ticket_page2.html", tickets=tickets.find(), title="Check Ticket")

@app.route("/view_ticket")
def view_ticket():
  guessed_nums.sort()
  return render_template("ticket_page.html", all_guessed_nums=guessed_nums)

@app.route("/get_random_num")
def get_random_num():
  random_num = random.randrange(1,11)
  guessed_nums.append(random_num)
  return redirect(url_for("view_ticket"))

def win(win_nums, guessed_nums):
  for i in range(len(win_nums)):
      if win_nums[i] != guessed_nums[i]:
          return False
  return True

@app.route("/check_ticket")
def check_ticket():
  all_guessed_nums = []

  for ticket in tickets.find({}):
    guessed_nums_temp = []
    guessed_nums_temp.append(int(ticket["number1"]))
    guessed_nums_temp.append(int(ticket["number2"]))
    guessed_nums_temp.append(int(ticket["number3"]))
    guessed_nums_temp.sort()
    all_guessed_nums.append(guessed_nums_temp)
    guessed_nums_temp = []
  
  win_times = check_all(winning_nums, all_guessed_nums)

  return render_template("test.html", win=win_times)

@app.route("/reset_num")
def reset_num():
  guessed_nums.clear()
  return redirect(url_for("view_ticket"))

if __name__ == "__main__":
    app.run(debug=True)



# all_guessed_nums = [2,3,7,9]
all_guessed_nums = [[2,3,4,5], [2,3,6], [2,3,5], [5,6,7,8]]

# random_guessed_nums = []

# def generate_random_num(times):
#   for _ in range(times):
#     random_num = random.randrange(1,11)
#     random_guessed_nums.append(random_num)

# generate_random_num(3)
# print(random_guessed_nums)




# print(win(winning_nums, all_guessed_nums))

def check_all(win_nums, guessed_nums_list):
  win_count = 0
  for i in range(len(guessed_nums_list)):
    if win(win_nums, guessed_nums_list[i]):
      win_count += 1
    # else:
      # print("you lose")
  return win_count

# print(f"You won {check_all(winning_nums, all_guessed_nums)} out of {len(all_guessed_nums)} plays.")
# print("For " + str(check_all(winning_nums, all_guessed_nums)/len(all_guessed_nums)) + " percent.")
# print((check_all(winning_nums, all_guessed_nums)/len(all_guessed_nums)))