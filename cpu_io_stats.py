""" Gathers IO wait and CPU stats which are then pickled to a specific file """

import argparse
import time
import pickle
import psutil


def main(output_file: str, interval: int, max_time:int):
    """Collect the stats and save to pickle files"""
    # Get the time in seconds
    start_time = time.time()

    # Where we'll keep the data
    cpu_usage = []
    io_wait = []

    print('Starting to collect the data...')

    # Run for the max time
    while time.time() < start_time + max_time:
        _cpu = psutil.cpu_percent()
        _io = psutil.cpu_times_percent().iowait
        cpu_usage.append(_cpu)
        io_wait.append(_io)

        # Sleep for the interval amount of seconds
        time.sleep(interval)

    f_name = output_file if '.pkl' in output_file else f'{output_file}.pkl'

    # Save the results to the specified file
    print(f'Finished running experiment after {time.time()-start_time} seconds')
    print(f'Saving results in a pickle file to {f_name}')

    f_name = output_file if '.pkl' in output_file else f'{output_file}.pkl'

    # build the dict with all the measurements
    measurements = {
        'cpu': cpu_usage,
        'iowait': io_wait
    }

    # Save the file in the specified folder
    with open(f_name, 'wb') as f:
        pickle.dump(measurements, f)


if __name__ == '__main__':
    # Read the arguments
    parser = argparse.ArgumentParser(description="Gather CPU and IO stats and output them to a file")
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Path to the output file to save (without format)')

    parser.add_argument('-i', '--interval',
                        type=int,
                        required=False,
                        default=2,
                        help='Time interval to save the current count in seconds')

    parser.add_argument('-m', '--max_time',
                        type=int,
                        required=False,
                        default=300,
                        help='Max time of running the experiment')

    args = parser.parse_args()

    main(args.output, args.interval, args.max_time)
