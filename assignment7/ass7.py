import matplotlib.pyplot as plt 
import numpy as np

def read_file(filename):
    # day of birth 23
    # month of birth 13-14
    # sex 475
    # birth weight 504-507

    results = {
        'M': {},
        'F': {}
    }

    with open(filename, "rb") as f:
        data = f.readline()
        while data:
            month = data[12:14].decode("utf-8")
            day = data[22:23].decode('utf-8')
            sex = data[474:475].decode('utf-8')
            birth_weight = data[503:507].decode('utf-8')

            if month not in results[sex]:
                results[sex][month] = {}

            if day not in results[sex][month]:
                results[sex][month][day] = {'weight':0,
                                            'number':0,
                                            }
            results[sex][month][day]['weight'] += int(birth_weight)
            results[sex][month][day]['number'] += 1

            data = f.readline()

    
    return results


def plot_data(data, year):
    weight = 0
    number = 0
    female_days = list(range(1,8))
    male_days = list(range(1,8))
    female_weight = list(range(1,13))
    male_weight = list(range(1,13))
    female_tot = 0
    male_tot = 0


    for sex in data:
        months = data[sex]
        for month in months:
            days = months[month]
            for day in days:   
                if sex == "M":
                    male_days[int(day) -1] += int(days[day]['number'])
                
                elif sex == "F":
                    female_days[int(day)-1] += int(days[day]['number'])
                weight += int(days[day]['weight'])
                number += int(days[day]['number'])
            

            if sex == "M":
                male_weight[int(month) -1] += weight/number
                male_tot += number
            
            elif sex == "F":
                female_weight[int(month)-1] += weight/number
                female_tot += number

            weight = 0
            number = 0

    width = 0.35
    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    days_name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    # Plot the average weight

    plt.figure()
    plt.title("Average weight in " + year)
    plt.bar(np.arange(1, 13), male_weight,width, label="Male")
    plt.bar(np.arange(1, 13) + width, female_weight, width, label="Female")
    plt.xticks(list(range(1,13)), month_name)
    plt.legend(loc="best")
    plt.ylim(0, 5000)
    plt.savefig("average_weight_" + year + ".png")
    plt.close()

    # Plot the days people are born in

    plt.figure()
    plt.title("Days born in " + year)
    plt.bar(np.arange(1, 8), male_days, width, label="Male")
    plt.bar(np.arange(1, 8) + width, female_days, width, label="Female")
    plt.legend(loc="best")
    plt.xticks(list(range(1,8)), days_name)
    plt.ylim(0, 500000)
    plt.savefig("days_born" + year + ".png")
    plt.close()

    # Plot the propotion of guys versus girls
    plt.figure()
    plt.title("Proportions " + year)
    plt.bar(np.arange(1), (male_tot / (male_tot + female_tot)) * 100, width, label="Male")
    plt.bar(np.arange(1) + width, (female_tot / (male_tot + female_tot)) * 100, width, label="Female")
    plt.legend(loc="best")
    plt.xticks(np.arange(1), year)
    plt.ylim(0, 80)
    plt.savefig("prop_born" + year + ".png")
    plt.close()

df2019 = read_file("Nat2019.txt")
df2018 = read_file("Nat2018.txt")

plot_data(df2019, "2019")
plot_data(df2018, "2018")