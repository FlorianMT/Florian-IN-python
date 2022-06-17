import asyncio # voor het draaien van de quicksort functie
import matplotlib.pyplot as plt # voor het renderen van de visualisatie
import random # genereren van een random array
from numpy.random import shuffle # voor het shuffelen

# global variables
Array = []
bars = []
fig = 0

def getArray():
    """
    Functie voor ophalen van input array
    """
    global Array
    print("Please enter a starting array. values are separated by commas and no spaces are allowed.")
    print("Type 'random' to use a randomly generated array.")
    print("Example input: '1,6,4,2,7,8,5'")
    # zolang nog geen valide array opgehaalt is zal dit blijven loopen
    while True:
        ArrayString = input(":> ")
        if ArrayString != "random":
            Array = ArrayString.strip(',').split(',')
            try:
                # conversie van strings array naar een number array. Als hierbij een ValueError voorkomt catch ik die
                Array = [int(n) for n in Array]
                break
            except ValueError:
                print("Your input is invalid. Try again")
        else:
            # generatie van random array
            Array = [i for i in range(1,60)]
            shuffle(Array) # uit numpy
            break

def getSort():
    """
    Functie voor ophalen van het sorting algoritme
    """
    # alle mogenlijke algorithms. dit moet in lowercase
    algos = [
        "quicksort",
        "bubblesort",
        "mergesort"
    ]

    print("Please enter the sorting algorithm you would like to visualize.")
    # hier print ik alle mogelijke aglos uit algos 
    str = 'Available sorting algorithms are: '
    for i in algos:
        str += i + ", "
    str = str.strip(', ') # hiermee haal ik de laatse comma weg (is wat mooier)
    print(str)
    # blijft loopen tot de gebruiker een kloppend antwoord heeft gegeven
    while True:
        SortString = input(":> ")
        # check of 
        if SortString.lower() in algos:
            return SortString
        print("Your input is invalid. Try again")

def getShuffle():
    """
    Functie om aan de gebruiker te vragen of diegene nog een keer wilt sorteren.
    """
    while True:
        print("Would you like to shuffle the array and sort again? yes or no")
        shuffleInput = input(":> ")
        if shuffleInput.lower() == "yes":
            return True
        elif shuffleInput.lower() == "no":
            return False
        print("Your input is invalid. Try again")

async def mergeSort(arr):
    """
    Algorithm source: https://www.geeksforgeeks.org/merge-sort/
    """
    if len(arr) > 1:
        mid = len(arr)//2

        leftportion = arr[:mid]
        rightportion = arr[mid:]

        await mergeSort(leftportion)
        await mergeSort(rightportion)

        i = j = k = 0
        while i < len(leftportion) and j < len(rightportion):
            if leftportion[i] < rightportion[j]:
                arr[k] = leftportion[i]
                i += 1
            else:
                arr[k] = rightportion[j]
                j += 1
            for n in range(len(bars)):
                bars[n].set_height(Array[n])
                bars[n].set_color('b')
            bars[k].set_color("r")
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.0000001)
            k += 1

        while i < len(leftportion):
            arr[k] = leftportion[i]
            for n in range(len(bars)):
                bars[n].set_height(Array[n])
                bars[n].set_color('b')
            bars[k].set_color("r")
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.0000001)
            i += 1
            k += 1

        while j < len(rightportion):
            arr[k] = rightportion[j]
            for n in range(len(bars)):
                bars[n].set_height(Array[n])
                bars[n].set_color('b')
            bars[k].set_color("r")
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.0000001)
            j += 1
            k += 1

async def bubbleSort():
    """
    Algorithm source: https://www.geeksforgeeks.org/bubble-sort/
    """
    for i in range(len(Array)):
        for j in range(0,len(Array)-i-1):
            if Array[j] > Array[j+1]:
                (Array[j], Array[j+1]) = (Array[j+1], Array[j])
                for n in range(len(bars)):
                    bars[n].set_height(Array[n])
                    bars[n].set_color('b')
                bars[j].set_color("r")
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.0000001)
    for n in range(len(bars)):
        bars[n].set_height(Array[n])
        bars[n].set_color('b')
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.0001)

async def quickSort(low, high):
    """
    Quicksort functie.
    algorithm source: https://textbooks.cs.ksu.edu/cc310/7-searching-and-sorting/19-quicksort-pseudocode/
    """
    if low < high:
        pi = await partition(low, high)
        await quickSort(low, pi-1)
        await quickSort(pi + 1, high)
        for n in range(len(bars)):
            bars[n].set_height(Array[n])
            bars[n].set_color('b')
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.0001)

async def partition(low, high):
    global bars
    pivot = Array[high]
    i = low-1
    for j in range(low, high):
        if Array[j] < pivot:
            i+=1
            (Array[j], Array[i]) = (Array[i], Array[j])
            for n in range(len(bars)):
                bars[n].set_height(Array[n])
                bars[n].set_color('b')
            bars[i].set_color("r")
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.0000001)
    (Array[i + 1], Array[high]) = (Array[high], Array[i + 1])
    return i+1

async def handleCommands():
    while True:
        # haal het gekozen algoritme op
        sort = getSort()
        # check welk algoritme er gekozen is en voer de passende functie uit
        if sort == "quicksort":
            await quickSort(0, len(Array)-1)
        elif sort == "bubblesort":
            await bubbleSort()
        elif sort == "mergesort":
            await mergeSort(Array)
        if not getShuffle(): break # als de gebruiker niet nog een keer wilt sorteren zal de loop eindigen
        shuffle(Array) # uit numpy
    print("Goodbye") # wanneer de loop eindigd stopt ook het programma
    exit()


if __name__ == '__main__':
    getArray() # als eerst haal ik het array op

    fig = plt.figure()
    # hier maak ik alle bars aan
    bars = plt.bar(range(len(Array)), Array)

    # start de async functie handleCommands. Dit moet asynchronously gebeuren omdat plt.show() tegelijkertijd moet kunnen draaien 
    asyncio.run(handleCommands())

    plt.show()
    

