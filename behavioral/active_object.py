import threading
import queue
import time

class Future:
    """
    A class to hold the result of an asynchronous operation.

    Attributes
    ----------
    _result : Any
        The result of the asynchronous operation.
    _condition : threading.Condition
        Condition variable to manage thread synchronization.

    Methods
    -------
    set_result(result)
        Sets the result of the operation and notifies waiting threads.
    get_result()
        Waits for and returns the result of the operation.
    """

    def __init__(self):
        """
        Initializes the Future object with no result and a condition variable.
        """
        self._result = None
        self._condition = threading.Condition()

    def set_result(self, result):
        """
        Sets the result of the operation and notifies all waiting threads.

        Parameters
        ----------
        result : Any
            The result to be set and retrieved later by `get_result`.
        """
        with self._condition:
            self._result = result
            self._condition.notify_all()

    def get_result(self):
        """
        Waits for the result of the operation to be available and returns it.

        Returns
        -------
        Any
            The result of the operation.
        """
        with self._condition:
            while self._result is None:
                self._condition.wait()
            return self._result

class MethodRequest:
    """
    Represents a request to execute a method on the Servant.

    Attributes
    ----------
    servant : Any
        The target object on which the method is to be executed.
    method : callable
        The method to be executed.
    args : tuple
        The positional arguments for the method.
    kwargs : dict
        The keyword arguments for the method.
    priority : int
        The priority of the method request (higher value means higher priority).
    future : Future
        Future object to hold the result of the method execution.

    Methods
    -------
    execute()
        Executes the method on the servant and stores the result in the Future.
    """

    def __init__(self, servant, method, args=(), kwargs={}, priority=0):
        """
        Initializes the MethodRequest with the target servant, method, arguments, and priority.

        Parameters
        ----------
        servant : Any
            The target object on which the method is to be executed.
        method : callable
            The method to be executed.
        args : tuple, optional
            The positional arguments for the method (default is ()).
        kwargs : dict, optional
            The keyword arguments for the method (default is {}).
        priority : int, optional
            The priority of the method request (default is 0).
        """
        self.servant = servant
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.priority = priority
        self.future = Future()

    def execute(self):
        """
        Executes the method on the servant and stores the result in the Future.
        """
        result = self.method(self.servant, *self.args, **self.kwargs)
        self.future.set_result(result)

    def __lt__(self, other):
        """
        Compares MethodRequest objects based on priority for use in a priority queue.

        Parameters
        ----------
        other : MethodRequest
            Another MethodRequest object to compare with.

        Returns
        -------
        bool
            True if this object's priority is higher than the other.
        """
        return self.priority > other.priority  # Higher priority first

class Scheduler(threading.Thread):
    """
    Scheduler that manages the execution of MethodRequests using a priority queue.

    Attributes
    ----------
    activation_queue : queue.PriorityQueue
        A priority queue to store and order MethodRequest objects.

    Methods
    -------
    enqueue(method_request)
        Adds a MethodRequest to the activation queue.
    run()
        Continuously processes MethodRequests from the activation queue.
    """

    def __init__(self):
        """
        Initializes the Scheduler and starts it as a daemon thread.
        """
        super().__init__()
        self.activation_queue = queue.PriorityQueue()
        self.daemon = True  # Allows the thread to be killed when the main thread exits
        self.start()

    def enqueue(self, method_request):
        """
        Adds a MethodRequest to the activation queue for execution.

        Parameters
        ----------
        method_request : MethodRequest
            The MethodRequest object to be enqueued.
        """
        self.activation_queue.put(method_request)

    def run(self):
        """
        Continuously processes MethodRequests from the activation queue.
        """
        while True:
            method_request = self.activation_queue.get()
            method_request.execute()

class TransactionProcessor:
    """
    The Servant class that contains the actual transaction processing logic.

    Methods
    -------
    process_transaction(transaction_id, amount)
        Processes a financial transaction with the given ID and amount.
    """

    def process_transaction(self, transaction_id, amount):
        """
        Simulates the processing of a financial transaction.

        Parameters
        ----------
        transaction_id : str
            The ID of the transaction to be processed.
        amount : float
            The amount of the transaction.

        Returns
        -------
        str
            A confirmation message indicating the transaction is complete.
        """
        print(f"Processing transaction {transaction_id} for amount ${amount}...")
        time.sleep(2)  # Simulate a time-consuming transaction
        return f"Transaction {transaction_id} completed for ${amount}."

class Proxy:
    """
    Proxy class that interfaces with clients and submits method requests to the scheduler.

    Attributes
    ----------
    scheduler : Scheduler
        The scheduler responsible for managing and executing MethodRequests.
    servant : TransactionProcessor
        The servant that processes transactions.

    Methods
    -------
    process_transaction(transaction_id, amount, priority=0)
        Submits a transaction processing request to the scheduler.
    """

    def __init__(self, scheduler, servant):
        """
        Initializes the Proxy with a Scheduler and a TransactionProcessor.

        Parameters
        ----------
        scheduler : Scheduler
            The scheduler responsible for managing and executing MethodRequests.
        servant : TransactionProcessor
            The servant that processes transactions.
        """
        self.scheduler = scheduler
        self.servant = servant

    def process_transaction(self, transaction_id, amount, priority=0):
        """
        Submits a transaction processing request to the scheduler.

        Parameters
        ----------
        transaction_id : str
            The ID of the transaction to be processed.
        amount : float
            The amount of the transaction.
        priority : int, optional
            The priority of the transaction (default is 0).

        Returns
        -------
        Future
            A Future object to retrieve the result of the transaction processing.
        """
        method_request = MethodRequest(self.servant, TransactionProcessor.process_transaction, 
                                       (transaction_id, amount), priority=priority)
        self.scheduler.enqueue(method_request)
        return method_request.future

# Example usage
if __name__ == "__main__":
    transaction_processor = TransactionProcessor()
    scheduler = Scheduler()
    proxy = Proxy(scheduler, transaction_processor)

    # Make asynchronous calls with different priorities
    future_high = proxy.process_transaction("T1001", 10000, priority=10)  # High priority
    future_low = proxy.process_transaction("T1002", 500, priority=1)  # Low priority
    future_medium = proxy.process_transaction("T1003", 3000, priority=5)  # Medium priority

    # Do other things here...
    print("System is processing transactions while you do other tasks...")

    # Retrieve results
    print(future_high.get_result())
    print(future_medium.get_result())
    print(future_low.get_result())
