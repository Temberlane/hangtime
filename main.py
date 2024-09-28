import datetime
#Uses rate my professor module
import ratemyprofessor
from website import create_app

# stuff to actually run the website below very important
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

class lectures:
    def __init__(self, courseCode, instructor, startTime, endTime, profRating):
        self.courseCode = courseCode
        self.instructor = instructor
        self.profRating = profRating
        self.startTime = startTime
        self.endTime = endTime
        self.date = startTime.date()
    def __str__(self):
        return f"{self.courseCode} , taught by {self.instructor} with a rating of {self.profRating}"
    #Setter for Course Start Time
    def setStartTime(self, year, month,day,hour,minute):
        self.startTime = datetime.datetime(year, month, day, hour, minute)
    #Setter for course end time
    def setEndTime(self, year, month,day,hour,minute):
        self.endTime = datetime.datetime(year, month, day, hour, minute)
    #retuns class duration
    def classDuration(self):
        return self.endTime - self.startTime
    def setProfRating(self):
        userInstitute  = ratemyprofessor.get_school_by_name("University of Ottawa")
        profName = ratemyprofessor.get_professor_by_school_and_name(userInstitute, self.instructor)
        self.profRating = profName.rating


    def getStartTimne(self):
        return self.startTime

    def getEndTimne(self):
        return self.getEndTimne

    def getDate(self):
        return self.startTime.date()


class lectureAddtives(lectures):
    def __init__(self, courseCode, instructor, startTime, endTime, date):
        super().__init__(courseCode, instructor, startTime, endTime, date, None)
        def __str__(self):
            return f"This is a lecture additive for {self.courseCode} taught by {self.instructor}."

# startTime1 = datetime.datetime(2024, 7, 18, 5, 4, 20)
# endTime1 = datetime.datetime(2024, 7, 18, 6, 4, 20)

# lec1 = lectures("CHM1311", "Vida Dujmovic", startTime1, endTime1,  5.0)
# lec1.setProfRating()
