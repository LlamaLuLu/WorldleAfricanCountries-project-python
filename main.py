# 22/6/2023

import turtle as t
import pandas
import time
import random
COLOURS = ["red", "black", "green", "blue", "brown"]

# idea: make SA cities ver.

def revise_answers(correct, countries_list):
    """Saves all countries that were not guessed into csv file for player to revise."""
    for c in correct:
        countries_list.remove(c)
    data = pandas.DataFrame(countries_list)
    data.to_csv("countries_to_learn.csv")


def check_high_score(correct, best):
    """Checks if new record was made after game over."""
    if len(correct) > best:
        best = len(correct)
        with open("high_score.txt", "w") as f:
            f.write(str(best))
        # show new record
        new_rec = t.Turtle()
        new_rec.hideturtle()
        new_rec.penup()
        new_rec.goto(new_rec.xcor(), 100)
        new_rec.write(f"You made the new high score!\nYour score was: {best}", align="center",
                         font=("Courier", 27, "normal"))
        screen.update()
        time.sleep(5)
    elif len(correct) == best:
        new_rec = t.Turtle()
        new_rec.hideturtle()
        new_rec.penup()
        new_rec.goto(new_rec.xcor(), 100)
        new_rec.write(f"Your score was: {best}\nlike the previous high score!", align="center",
                         font=("Courier", 27, "normal"))
        time.sleep(5)

# move textbox to corner

screen = t.Screen()
screen.title("Worldle Game: Are you really African?")
image = "countries_resized.gif"
screen.addshape(image)
t.shape(image)
screen.setup(width=750, height=765)
screen.tracer(0)

chance = 3  # show lives on screen
lives = t.Turtle()
lives.hideturtle()
lives.penup()
lives.goto(-250, -335)
lives.write(f"Lives left: {chance}", align="center", font=("Courier", 25, "normal"))
screen.update()

data = pandas.read_csv("African countries.csv")
all_countries = data.Country.to_list()
with open("high_score.txt") as f:  # shows high score
    high_score = int(f.read())

answer = screen.textinput(title="Guess the countries", prompt=f"Your high score is: {high_score}"
                                                              f"\nStart by naming an African country:")
correct_answers = []
game_on = True
while game_on:
    answer = answer.title()
    if len(correct_answers) == 54:  # won
        game_on = False
        winner = t.Turtle()
        winner.hideturtle()
        winner.write("WELL DONE!\nYou knew all the countries.\nYou are now a true African.", align="center",
                     font=("Courier", 25, "normal"))
        screen.update()
        time.sleep(6)
    elif answer == "Exit":  # quit
        game_on = False
        revise_answers(correct_answers, all_countries)
        check_high_score(correct_answers, high_score)
    else:  # guessing
        if answer in all_countries:  # correct
            if answer in correct_answers:  # duplicate answer
                answer = screen.textinput(title=f"{len(correct_answers)}/50 Countries Correct",
                                                prompt="You've already guessed that.\nWhat's another country's name? ")
                continue
            correct_answers.append(answer)  # record correct guess

            country_name = t.Turtle()  # reveal country name
            country_name.hideturtle()
            country_name.speed("fastest")
            country_name.color(random.choice(COLOURS))
            country_name.penup()
            country_data = data[data.Country == answer]  # get co-ords for country_name
            x_cor, y_cor = int(country_data.x.iloc[0]), int(country_data.y.iloc[0])
            country_name.goto(x_cor, y_cor)
            # to get indiv item from data -> .item()
            country_name.write(f"{country_data.Country.item()}\n{country_data.Capital.item()}",
                               align="center", font=("Courier", 10, "normal"))  # shows capital city

            screen.update()
            time.sleep(.7)
            answer = screen.textinput(title=f"{len(correct_answers)}/50 Countries Correct",
                                            prompt="That's correct!\nWhat's another country's name? ")
        else:  # wrong
            chance -= 1
            lives.clear()
            lives.write(f"Lives left: {chance}", align="center", font=("Courier", 25, "normal"))
            screen.update()
            if chance == 0:  # lose
                game_on = False
                loser = t.Turtle()
                loser.hideturtle()
                loser.write("YOU LOSE!\nA true African must revise the countries\nthey don't know.",
                            align="center", font=("Courier", 25, "normal"))
                screen.update()
                time.sleep(6)
                revise_answers(correct_answers, all_countries)
                check_high_score(correct_answers, high_score)
            elif chance == 1:
                answer = screen.textinput(title=f"{len(correct_answers)}/50 Countries Correct",
                                          prompt="That's incorrect... This is your LAST life!"
                                                 "\nWhat's another country's name? ")
            else:
                answer = screen.textinput(title=f"{len(correct_answers)}/50 Countries Correct",
                                          prompt=f"That's incorrect... You have {chance} lives "
                                                 f"left.\nWhat's another country's name? ")
