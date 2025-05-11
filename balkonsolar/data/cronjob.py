
from apscheduler.schedulers.background import BackgroundScheduler
from store_data_for_scheduling import main as store_data_for_scheduling
import multiprocessing
from datetime import datetime


def main():
        #script_cop
    scheduler = BackgroundScheduler()
    scheduler.add_job(call_timeout, 'interval', minutes=30, misfire_grace_time=60, next_run_time=datetime.now(), args=(20, store_data_for_scheduling))


def call_timeout(timeout, func):

    if type(timeout) not in [int, float] or timeout <= 0.0:
        print("Invalid timeout!")

    elif not callable(func):
        print("{} is not callable!".format(type(func)))

    else:
        p = multiprocessing.Process(target=func)
        p.start()
        p.join(timeout)

        if p.is_alive():
            p.terminate()
            print("Process {} timed out after {} seconds".format(func.__module__, timeout))
            #multi_logger.error("Process {} timed out after {} seconds".format(func.__module__, timeout))
            #scripts_and_authors.mail_author_database("Process {} timed out after {} seconds".format(func.__module__, timeout), func.__module__)

        else:
            if p.exitcode != 0:
                # Process terminated with an error
                print(f"Process terminated with exit code {p.exitcode}")
                #multi_logger.error(f"Script {func.__module__} has exit code: {p.exitcode}")
                #scripts_and_authors.mail_author_database(f"Script {func.__module__} has exit code: {p.exitcode}", func.__module__)

        return None
        #     return False
        # else:
        #     return True


if __name__ == '__main__':

    main()

