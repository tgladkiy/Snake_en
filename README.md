# Snake_en

The program is a simulator for teaching AI to play the snake game.  
Video: <a>https://youtu.be/LKOb5cC6hZk</a>

<b>Files and modules:</b>  
`snake_main_en.py` - main file  
`snake_matrix_en.py` - game field and snake. Forms a matrix of the playing field, generates apples, stores information about the state and current position of the 
snake, calculates sensor data  
`rnd_snakes_en.py` - multiprocessing generation of zero populations, selects best snakes in families  
`snake_ai_en.py` – neural network, predicting the next move  
`snake_draw_en.py` - renrering the game window, drawing animation and tables  
`plot_to_img_en.py` - the script opens in a separate process, generates a plot and saves it to a file.  
`snake_plot_clean.png` - picture with an empty plot  
`snake_plot.png` - plot with results, updated after each epoch  
`snake_best_weights_ХХХХХХ_ХХХХ.bin` - file with weights and results, generated every time the program is launched  
`snake_statistics_ХХХХХХ_ХХХХ.csv` - file with game statistics  

<b>Standard and popular libraries:  </b>  
`os, time, datetime, pickle, shutil` – window placement, time, date and working with files (saving weights, statistics, graphs, copying)  
`pygame` – game window, animation, output of result tables  
`pandas, matplotlib` – working with data and plot   
`multiprocessing` – creating multiple threads to calculate random weights for several families simultaneously  
`subprocess` – creates a process, opens the plotting script, saves the plot to a file  

<b>Algorithm:</b>  
Each snake is a perceptron with 2 hidden layers, 1 input sensors layer and 1 direction layer.  
Stages:  
- several families are formed from a large number of snakes with random weights (10.000-100.000)
- selection of snakes with the best results
- multiple crossing of snakes in each family + mutation 1-5% and selection of the best by scores and moves
- crossing the best snakes from families after 100 epochs - forming a Super-Family
- endless cycle: games - selection the best snakes - crossing - games
