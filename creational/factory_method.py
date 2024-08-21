from abc import ABC, abstractmethod

class Interviewer(ABC):
    """
    Abstract base class representing an interviewer.

    Methods
    -------
    askQuestions()
        Abstract method to ask questions during an interview.
    """

    @abstractmethod
    def askQuestions(self):
        """
        Ask questions during an interview.

        This method should be implemented by subclasses to provide specific interview questions.
        """
        pass


class Developer(Interviewer):
    """
    Concrete class representing a Developer interviewer.

    Methods
    -------
    askQuestions()
        Asks development-related questions during an interview.
    """

    def askQuestions(self):
        """
        Asks development-related questions during an interview.
        """
        print("Asking development-related questions.")


class CommunityExecutive(Interviewer):
    """
    Concrete class representing a Community Executive interviewer.

    Methods
    -------
    askQuestions()
        Asks community-related questions during an interview.
    """

    def askQuestions(self):
        """
        Asks community-related questions during an interview.
        """
        print("Asking community-related questions.")


class HiringManager(ABC):
    """
    Abstract base class representing a hiring manager.

    Attributes
    ----------
    interviewer : Interviewer
        An instance of the Interviewer class.

    Methods
    -------
    makeInterviewer()
        Abstract method to create an interviewer.
    takeInterview()
        Conducts an interview by asking questions through the interviewer.
    """

    def __init__(self):
        """
        Initializes the HiringManager with a placeholder interviewer.
        """
        self.interviewer = None

    @abstractmethod
    def makeInterviewer(self):
        """
        Creates an interviewer.

        This method should be implemented by subclasses to provide specific interviewer instances.
        """
        pass

    def takeInterview(self):
        """
        Conducts an interview by creating an interviewer and asking questions.
        """
        self.interviewer = self.makeInterviewer()
        self.interviewer.askQuestions()


class DevelopmentManager(HiringManager):
    """
    Concrete class representing a hiring manager for development roles.

    Methods
    -------
    makeInterviewer()
        Creates a Developer interviewer.
    """

    def makeInterviewer(self):
        """
        Creates and returns a Developer interviewer.

        Returns
        -------
        Developer
            An instance of the Developer class.
        """
        return Developer()


class MarketingManager(HiringManager):
    """
    Concrete class representing a hiring manager for marketing roles.

    Methods
    -------
    makeInterviewer()
        Creates a Community Executive interviewer.
    """

    def makeInterviewer(self):
        """
        Creates and returns a Community Executive interviewer.

        Returns
        -------
        CommunityExecutive
            An instance of the Community Executive class.
        """
        return CommunityExecutive()


# Example usage
if __name__ == "__main__":
    devManager = DevelopmentManager()
    devManager.takeInterview()

    marketingManager = MarketingManager()
    marketingManager.takeInterview()
