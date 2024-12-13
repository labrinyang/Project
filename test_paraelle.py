import multiprocessing
import time

# square function
def square(x):
    return x * x


if __name__ == '__main__':

    # multiprocessing pool object
    pool = multiprocessing.Pool()

    # input list
    inputs = [1]

    now = time.time()

    # map the function to the list and pass
    # function and input list as arguments
    outputs = pool.map_async(square, inputs)
    

    # Print input list
    print("Input: {}".format(inputs))

    # Print output list
    print("Output: {}".format(outputs))

    counter = Counter(Xts)

    plt.bar(counter.keys(), [freq/num_trials for freq in counter.values()])
    plt.xlabel('Position')
    plt.ylabel('Frequency')
    plt.title(f'Position Distribution at time {T}')
    plt.show()

    print(f"Time used: {time.time() - now}")