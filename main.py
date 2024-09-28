import datetime
from website import create_app

# stuff to actually run the website below very important
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

class lectures:
    def __init__(self, courseCode, instructor, startTime, endTime, date, profRating):
        self.courseCode = courseCode
        self.instructor = instructor
        self.profRating = profRating
        self.startTime = startTime
        self.endTime = endTime
        self.date = date
    def __str__(self):
        return f"{self.courseCode} , taught by {self.instructor} with a rating of {self.profRating}"



class lectureAddtives(lectures):
    def __init__(self, courseCode, instructor, startTime, endTime, date):
        super().__init__(courseCode, instructor, startTime, endTime, date, None)
        def __str__(self):
            return f"This is a lecture additive for {self.courseCode} taught by {self.instructor}."

startTime1 = datetime.datetime(2024, 7, 18, 5, 4, 20)
endTime1 = datetime.datetime(2024, 7, 18, 6, 4, 20)


lec1 = lectures("GNG1105", "Arshan", startTime1, endTime1, startTime1.date(), 5.0)