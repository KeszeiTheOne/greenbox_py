from sensor import DS18B20

ds = DS18B20('28-00000800d250')
t = ds.temperature()  # read temperature

print(t)    # this is a namedtuple
print(t.C)  # Celcius
print(t.F)  # Fahrenheit
print(t.K)  # Kelvin
