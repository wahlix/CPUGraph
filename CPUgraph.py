# Library imports
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import time

# Bygg funktion för inhämning av processinfo
def get_proc_info():
    powershell_command = "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 | Select-Object -First 10 Name, CPU"
    process = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True)

    if process.returncode == 0:
        return process.stdout
    else:
        raise Exception(process.stderr)

# Samla in data från funktion
data = []
for _ in range(5): # Funktionen repeteras 5 ggr
    output = get_proc_info()
    lines = output.strip().split('\n')[3:]  # Ignorera header
    for line in lines:
        parts = line.split()
        data.append({'Name': ' '.join(parts[:-1]), 'CPU': float(parts[-1].replace(',', '.'))})
    time.sleep(10)

# Konvertera till DataFrame
 
df = pd.DataFrame(data) 
 
# Gruppera och summera CPU-användning per process
 
grouped_df = df.groupby('Name').sum().reset_index() 
 
# Sortera och välj topp 10 processer
 
top_processes = grouped_df.sort_values(by='CPU', ascending=False).head(10) 
 
# Skapa en stapeldiagram
 
plt.figure(figsize=(10, 8)) 
plt.barh(top_processes['Name'], top_processes['CPU']) 
plt.xlabel('Total CPU Time')
plt.ylabel('Process') 
plt.title('Top 10 CPU-consuming Processes Over Time') 
plt.gca().invert_yaxis()  

# Visa den högsta förbrukaren överst
plt.show()
