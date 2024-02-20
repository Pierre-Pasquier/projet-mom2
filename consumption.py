import pandas as pd
import matplotlib.pyplot as plt

# Specify the file path
file_path = "2012-2013 Solar home electricity data v2.csv"

# Load the data into a DataFrame
data = pd.read_csv(file_path)

a_csf = 0.05
b_csf = 0.05
c_csf = 0.05



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

# Plot the consumption and generation data for the first customer
plt.subplot(3, 1, 1)
plt.plot(hours, first_customer_consumption, label="Consumption")
plt.plot(hours, first_customer_generation, label="Generation")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Consumption and Generation for Customer 1")

# Plot the consumption and generation data for the second customer
plt.subplot(3, 1, 2)
plt.plot(hours, second_customer_consumption, label="Consumption")
plt.plot(hours, second_customer_generation, label="Generation")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Consumption and Generation for Customer 2")

# Plot the consumption and generation data for the third customer
plt.subplot(3, 1, 3)
plt.plot(hours, third_customer_consumption, label="Consumption")
plt.plot(hours, third_customer_generation, label="Generation")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Consumption and Generation for Customer 3")

plt.tight_layout()  # Adjust the spacing between subplots
plt.show()

remaining_power_1 = first_customer_generation - first_customer_consumption
remaining_power_2 = second_customer_generation - second_customer_consumption
remaining_power_3 = third_customer_generation - third_customer_consumption

plt.subplot(3, 1, 1)
plt.plot(hours, remaining_power_1, label="Remaining Power")
plt.plot(hours, [0 for i in range(48)], label="Zero line")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Remaining Power for Customer 1")

plt.subplot(3, 1, 2)
plt.plot(hours, remaining_power_2, label="Remaining Power")
plt.plot(hours, [0 for i in range(48)], label="Zero line")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Remaining Power for Customer 2")

plt.subplot(3, 1, 3)
plt.plot(hours, remaining_power_3, label="Remaining Power")
plt.plot(hours, [0 for i in range(48)], label="Zero line")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Remaining Power for Customer 3")

plt.tight_layout()  # Adjust the spacing between subplots
plt.show()

remaining_power_positive_1 = [-1*min(0, power) for power in remaining_power_1]
remaining_power_positive_2 = [-1*min(0, power) for power in remaining_power_2]
remaining_power_positive_3 = [-1*min(0, power) for power in remaining_power_3]

sum_power = [power_1 + power_2 + power_3 for power_1, power_2, power_3 in zip(remaining_power_positive_1, remaining_power_positive_2, remaining_power_positive_3)]

price_CSF_1 = [a_csf*power**2 + b_csf*power + c_csf for power in sum_power]

# Plot the price of remaining power for Customer 1
plt.subplot(2,1,1)
plt.plot(hours, price_CSF_1, label="Price of CSF")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Price")
plt.legend()
plt.title("Price of CSF")


remaining_power_negative_1 = [max(0, power) for power in remaining_power_1]
remaining_power_negative_2 = [max(0, power) for power in remaining_power_2]
remaining_power_negative_3 = [max(0, power) for power in remaining_power_3]

negative_power = [power_1 + power_2 + power_3 for power_1, power_2, power_3 in zip(remaining_power_negative_1, remaining_power_negative_2, remaining_power_negative_3)]

sigma_p = 1
tau_p = 0.5

price_RES_1 = []
for power in negative_power:
    if power < tau_p/2*sigma_p:
        price_RES_1.append(-sigma_p*power**2 + tau_p*power)
    else:
        price_RES_1.append(tau_p**2/(2*sigma_p))
    


# Plot the price of remaining power for Customer 1
plt.subplot(2,1,2)
plt.plot(hours, price_RES_1, label="Price of RES Power")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Price")
plt.legend()
plt.title("Price of RES Power")
plt.tight_layout()  # Adjust the spacing between subplots
plt.show()



bill_consumer_1 = []
for i in range(len(remaining_power_1)):
    if remaining_power_1[i] < 0:
        bill_with_CSF = -1*price_CSF_1[i]*remaining_power_1[i]
        bill_with_RES = -1*price_RES_1[i]*remaining_power_1[i]
        if bill_with_RES == 0:
            bill_consumer_1.append(bill_with_CSF)
        else:
            bill_consumer_1.append(min(bill_with_CSF, bill_with_RES))
    else:
        bill_consumer_1.append(0)
        
bill_consumer_2 = []
for i in range(len(remaining_power_2)):
    if remaining_power_2[i] < 0:
        bill_with_CSF = -1*price_CSF_1[i]*remaining_power_2[i]
        bill_with_RES = -1*price_RES_1[i]*remaining_power_2[i]
        if bill_with_RES == 0:
            bill_consumer_2.append(bill_with_CSF)
        else:
            bill_consumer_2.append(min(bill_with_CSF, bill_with_RES))
    else:
        bill_consumer_2.append(0)
        
bill_consumer_3 = []
for i in range(len(remaining_power_3)):
    if remaining_power_3[i] < 0:
        bill_with_CSF = -1*price_CSF_1[i]*remaining_power_3[i]
        bill_with_RES = -1*price_RES_1[i]*remaining_power_3[i]
        if bill_with_RES == 0:
            bill_consumer_3.append(bill_with_CSF)
        else:
            bill_consumer_3.append(min(bill_with_CSF, bill_with_RES))
    else:
        bill_consumer_3.append(0)
        
plt.subplot(3, 1, 1)
plt.plot(hours, bill_consumer_1, label="Bill")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Bill (€)")
plt.legend()
plt.title("Bill for Customer 1")

plt.subplot(3, 1, 2)
plt.plot(hours, bill_consumer_2, label="Bill")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Bill (€)")
plt.legend()
plt.title("Bill for Customer 2")

plt.subplot(3, 1, 3)
plt.plot(hours, bill_consumer_3, label="Bill")
plt.xlabel("Hour of the day (h)")
plt.ylabel("Bill (€)")
plt.legend()
plt.title("Bill for Customer 3")

plt.tight_layout()  # Adjust the spacing between subplots
plt.show()
