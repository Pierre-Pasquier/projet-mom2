import pandas as pd
import matplotlib.pyplot as plt

# Specify the file path
file_path = "2012-2013 Solar home electricity data v2.csv"

# Load the data into a DataFrame
data = pd.read_csv(file_path)

# Filter the data for the first three customers
first_customer = data[data['Customer'] == 1].head(3)
second_customer = data[data['Customer'] == 2].head(3)
third_customer = data[data['Customer'] == 3].head(3)


first_customer_consumption = first_customer[first_customer['Consumption Category'] == 'GC'].values[0][5:-1]
first_customer_generation = first_customer[first_customer['Consumption Category'] == 'GG'].values[0][5:-1]

second_customer_consumption = second_customer[second_customer['Consumption Category'] == 'GC'].values[0][5:-1]
second_customer_generation = second_customer[second_customer['Consumption Category'] == 'GG'].values[0][5:-1]

third_customer_consumption = third_customer[third_customer['Consumption Category'] == 'GC'].values[0][5:-1]
third_customer_generation = third_customer[third_customer['Consumption Category'] == 'GG'].values[0][5:-1]

hours = [i/2 for i in range(1, 49)]
print(first_customer[first_customer['Consumption Category'] == 'GC'].values[0])
print(len(hours))
print(first_customer_consumption)

# Plot the consumption and generation data for the first customer
plt.plot(hours, first_customer_consumption, label="Consumption")
plt.plot(hours, first_customer_generation, label="Generation")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.title("Consumption and Generation for Customer 1")
plt.show()

# Plot the consumption and generation data for the second customer
plt.plot(hours, second_customer_consumption, label="Consumption")
plt.plot(hours, second_customer_generation, label="Generation")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.title("Consumption and Generation for Customer 1")
plt.show()

# Plot the consumption and generation data for the third customer
plt.plot(hours, third_customer_consumption, label="Consumption")
plt.plot(hours, third_customer_generation, label="Generation")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.title("Consumption and Generation for Customer 1")
plt.show()

remaining_power_1 = first_customer_generation - first_customer_consumption
remaining_power_2 = second_customer_generation - second_customer_consumption
remaining_power_3 = third_customer_generation - third_customer_consumption

plt.plot(hours, remaining_power_1, label="Remaining Power")
plt.plot(hours, [0 for i in range(48)], label="Zero line")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.title("Remaining Power for Customer 1")
plt.show()

plt.plot(hours, remaining_power_2, label="Remaining Power")
plt.plot(hours, [0 for i in range(48)], label="Zero line")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.title("Remaining Power for Customer 2")
plt.show()

plt.plot(hours, remaining_power_3, label="Remaining Power")
plt.plot(hours, [0 for i in range(48)], label="Zero line")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.title("Remaining Power for Customer 3")
plt.show()



