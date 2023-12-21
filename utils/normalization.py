from datetime import datetime


class LowUpScaller:
    '''
        Class for data normalization which has lower and upper limit.

        This class provides functionality for normalizing and denormalizing data within a specified range.

        Attributes:
            lower_limit (float): The lower limit of the normalization range.
            upper_limit (float): The upper limit of the normalization range.

        Methods:
            normalize(values: List[float]) -> List[float]:
                Normalize a list of values within the specified range.

            denormalize(normalized_values: List[float]) -> List[float]:
                Denormalize a list of normalized values back to the original range.

            info():
                Display information about the normalization range.

        Example:
            # Create an instance of LowUpScaller
            normalization_obj = LowUpScaller(lower_limit=-80, upper_limit=80)

            # Normalize a list of values
            original_values = [-60, -40, 0, 20, 40, 60]
            normalized_values = normalization_obj.normalize(original_values)

            # Denormalize the normalized values
            denormalized_values = normalization_obj.denormalize(normalized_values)

            # Display information about the normalization range
            normalization_obj.info()

            # Display results
            print("Original Values:", original_values)
            print("Normalized Values:", normalized_values)
            print("Denormalized Values:", denormalized_values)
        '''

    def __init__(self, lower_limit, upper_limit):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def normalize(self, values):
        normalized_values = [(val - self.lower_limit) / (self.upper_limit - self.lower_limit) for val in values]
        return normalized_values

    def denormalize(self, normalized_values):
        denormalized_values = [
            val * (self.upper_limit - self.lower_limit) + self.lower_limit for val in normalized_values
        ]
        return denormalized_values

    def info(self):
        normalization_range = f"Normalization range: [{self.lower_limit}, {self.upper_limit}]"
        print(normalization_range)


# TODO: Need will write test for a class TimeNormalization
class TimeNormalization:
    """
       A class for normalizing and denormalizing date and time values within a specified range.

       Attributes:
           lower_limit (datetime): The lower limit of the time range for normalization.
           upper_limit (datetime): The upper limit of the time range for normalization.
           time_format (str): The format of the input time, with the default value set to "%Y-%m-%d %H:%M:%S".
           days_in_month_normal (dict): Number of days in each month for a normal year.
           days_in_month_leap (dict): Number of days in each month for a leap year.
           min_year (int): Minimum year for normalization.
           max_year (int): Maximum year for normalization.
           min_month (int): Minimum month (constant: 1).
           max_month (int): Maximum month (constant: 12).
           min_day (int): Minimum day (constant: 1).
           min_minute (int): Minimum minute (constant: 0).
           max_minute (int): Maximum minute (constant: 59).
           min_second (int): Minimum second (constant: 0).
           max_second (int): Maximum second (constant: 59).
           year_index (int): Index for the year component in date lists.
           month_index (int): Index for the month component in date lists.
           day_index (int): Index for the day component in date lists.
           minute_index (int): Index for the minute component in date lists.
           second_index (int): Index for the second component in date lists.

        Examples:
            # Creating an object of the TimeNormalization class with specified time range
            normalization_obj = TimeNormalization(
                lower_limit="2023-01-01 00:00:00",
                upper_limit="2025-12-31 23:59:59",
                time_format="%Y-%m-%d %H:%M:%S"
            )

            # Test data: a list of dates in the format [year, month, day, hour, minute, second]
            original_dates = ["2024-02-28 09:55:00", "2025-02-28 09:55:00"]

            # Separating and concatenating dates
            separated_dates = normalization_obj.separation(original_dates)
            concatenated_dates = normalization_obj.concatenation(separated_dates)

            # Normalizing and denormalizing dates
            normalized_dates = normalization_obj.normalize(separated_dates)
            denormalized_dates = normalization_obj.denormalize(normalized_dates)

            # Displaying the information about normalization
            normalization_obj.info()
       """

    def __init__(self, lower_limit, upper_limit, time_format="%Y-%m-%d"):
        self.lower_limit = datetime.strptime(lower_limit, time_format)
        self.upper_limit = datetime.strptime(upper_limit, time_format)
        self.time_format = time_format

        # Определение количества дней в месяце для обычного и високосного года
        self.days_in_month_normal = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }

        self.days_in_month_leap = {
            1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }

        # Минимальные и максимальные значения для нормализации
        self.min_year = self.separation([self.lower_limit.strftime(self.time_format)])[0][0]
        self.max_year = self.separation([self.upper_limit.strftime(self.time_format)])[0][0]
        self.min_month, self.max_month = 1, 12
        self.min_day = 1
        self.year_index, self.month_index, self.day_index = 0, 1, 2


    def is_leap_year(self, year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


    def separation(self, dates):
        separated_dates = [
            list(map(int, str(datetime.strptime(date, self.time_format).strftime('%Y-%m-%d')).split('-')))
            for date in dates
        ]
        return tuple(separated_dates)


    def concatenation(self, separated_dates):
        concatenated_dates = [
            datetime(*date).strftime(self.time_format)
            for date in separated_dates
        ]
        return concatenated_dates


    def normalize(self, dates):
        normalized_dates = []
        for date in dates:
            if self.is_leap_year(date[0]):
                max_day = self.days_in_month_leap[date[1]]
            else:
                max_day = self.days_in_month_normal[date[1]]
            print(self.min_year)
            year_norm = (date[self.year_index] - self.min_year) / (self.max_year - self.min_year)
            month_norm = (date[self.month_index] - self.min_month) / (self.max_month - self.min_month)
            day_norm = (date[self.day_index] - self.min_day) / (max_day - self.min_day)
            normalized_date = [year_norm, month_norm, day_norm]
            normalized_dates.append(normalized_date)
        print(normalized_dates)
        return normalized_dates

    def denormalize(self, normalized_dates):
        min_date = self.separation([self.lower_limit.strftime(self.time_format)])[0]
        max_date = self.separation([self.upper_limit.strftime(self.time_format)])[0]
        is_leap_year = self.is_leap_year(min_date[self.year_index])
        denormalized_dates = []

        for date in normalized_dates:
            denormalized_date = [
                int(date[self.year_index] *
                    (max_date[self.year_index] - min_date[self.year_index]) +
                    min_date[self.year_index]),

                int(date[self.month_index] *
                    (self.days_in_month_leap[self.month_index]
                     if is_leap_year else
                     self.days_in_month_normal[self.month_index] - 1) +
                    min_date[self.month_index]),

                int(date[self.day_index] *
                    (max_date[self.day_index] - min_date[self.day_index]) +
                    min_date[self.day_index]),

                int(date[self.day_index] *
                    (self.days_in_month_leap[self.month_index]
                     if is_leap_year else
                     self.days_in_month_normal[self.month_index] - 1) +
                    min_date[self.month_index])
            ]
            denormalized_dates.append(denormalized_date)
        print(denormalized_dates)
        return denormalized_dates


    def info(self):
        print(f"Lower Limit: {self.lower_limit.strftime(self.time_format)}")
        print(f"Upper Limit: {self.upper_limit.strftime(self.time_format)}")
        print(f"Time Format: {self.time_format}")
