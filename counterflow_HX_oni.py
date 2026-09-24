import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import proj3d

# This is a program which will calculate the ideal length of a counterflow heat exchanger for the game Oxygen Not Included.
# The program only considers the possibility of pipes inside metal tiles, not pipes on flowing liquid
# Note that it is only considering the case where the radiant pipes and the metal tiles are built from the same material.
# It is not 100% accurate, as the calculations in-game can slightly differ due to lag

# Here is all of the info you have to give

# Metal: The thermal properties of the metal tile and radiant pipe
Metal_TC = 0
Metal_SHC = 0

# Liquid: The thermal properties of the liquid you're cooling
Liquid_TC = 0
Liquid_SHC = 0
    # Temperature: The temperature at which comes the liquid in the counterflow heat exchanger (in °C)
Liquid_temperature = 0
    # Weight: the amount of liquid that flows in the pipes (in grams)  (useful for matching geysers outputs)
Liquid_weight = 0

# Coolant: The thermal properties of the coolant you're using
Coolant_TC = 0
Coolant_SHC = 0
    # Weight: the amount of coolant that flows in the pipes (in grams) (most often 10000 or 10 kg)
Coolant_weight = 0

# Coolant range: The desired minimum calculated temperature to the desired maximum calculated temperature (calculated by steps of 2°C)
# Currently, the code does not handle negative temperatures for the coolant, fixed soon!
Coolant_temp_minimum = 0
Coolant_temp_maximum = 0

# Interaction tests: the maximum amount of calculated "interaction blocks" (compound of the two metal tiles with the liquid and coolant pipes through each one of them)
# Always tests from 1 to the given amount
Interaction_tests = 0

# Ideal temperature range: the green area in the graph showing your desired ending liquid temperature range
# Only works if the temperature range is reachable for the liquid
Ideal_temperature_range_minimum = 0
Ideal_temperature_range_maximum = 0


# To read the graph, the green area is representing the solution which respect all of the ideal temperatures reached by the liquid at the end.
# You can use the "+" and "-" keys to rotate the graph


# The explanation section is over!
# If you have any problem, don't hesitate to contact me on my GitHub (https://github.com/HighlyFlammableHuman) or my reddit (u/HighlyFlammableHuman)




Coolant_temp_minimum //= 2
Coolant_temp_maximum = int((Coolant_temp_maximum / 2) + 1)
Interaction_tests += 1

with open("results.txt", "w") as fichier:
    pass

for coolant_temperature in range(Coolant_temp_minimum, Coolant_temp_maximum):
    for interaction_number in range(1, Interaction_tests):
        interact_nb = interaction_number
        coolant_temp = coolant_temperature*2
        liquid_temp = Liquid_temperature

        metal_tc = Metal_TC
        metal_shc = Metal_SHC


        materials = {
            "coolant": {
                "tc": Coolant_TC,
                "shc": Coolant_SHC,
                "weight": Coolant_weight
            },
            "liquid": {
                "tc": Liquid_TC,
                "shc": Liquid_SHC,
                "weight": Liquid_weight
            }
        }

        interact = {
        }

        for i in range(interact_nb):
            interact[i+1] = { 
                    "coolant": {
                        "temp" : coolant_temp,
                        "p_temp" : coolant_temp,
                        "t_temp" : coolant_temp,
                    },
                    "liquid":{ 
                        "temp" : liquid_temp,
                        "p_temp" : liquid_temp,
                        "t_temp" : liquid_temp,
                    }
                }
            





        delta_t = 0.2

        def k_min (k1, k2):
            k_result = min(k1,k2)
            return k_result

        def k_geom (k1, k2):
            k_result = math.sqrt(k1 * k2)
            return k_result

        def k_avg (k1, k2):
            k_result = (k1 + k2)/2
            return k_result

        def k_mult (k1, k2):
            k_result = (k1 * k2)/2
            return k_result

        def Cth_max (temp1, temp2, m_scale1, m_scale2, m1, m2, shc1, shc2, area1, area2):
            if max(temp1, temp2) == temp1:
                s = m_scale1
                m = m1
                shc = shc1
                A = area1
            else:
                s = m_scale2
                m = m2
                shc = shc2
                A = area2
            result = s*((m*shc)/A)
            return result

        #interact type: building <-> cell = 0
        #               solid <-> solid = 1
        #               radiant pipe <-> pipe content = 2
        def TC_calcul_building_cell(k1, k2, temp1, temp2, m_scale1, m_scale2, m1, m2, shc1, shc2, area1, area2):
            if temp1 >= temp2:
                delta_T = temp1 - temp2
            else:
                delta_T = temp2 - temp1
            q = delta_T * delta_t * k_mult (k1, k2) * Cth_max(temp1, temp2, m_scale1, m_scale2, m1, m2, shc1, shc2, area1, area2)
            return q

        def TC_calcul_solid_solid(k1, k2, temp1, temp2):
            if temp1 >= temp2:
                delta_T = temp1 - temp2
            else:
                delta_T = temp2 - temp1
            q = delta_T * delta_t * k_geom (k1, k2) * 1000.0
            return q

        def TC_calcul_rpipe_pipecont(k1, k2, temp1, temp2):
            if temp1 >= temp2:
                delta_T = temp1 - temp2
            else:
                delta_T = temp2 - temp1
            q = delta_T * delta_t * k_avg (k1, k2) * 100.0
            return q

        def SHC_calcul(q, m1, m2, shc1, shc2, temp1, temp2):
            thc1 = m1 * shc1
            thc2 = m2 * shc2
            equi_temp = ((thc1 * temp1) + (thc2 * temp2)) / (thc1 + thc2)
            q_max = abs(thc1 * (temp1 - equi_temp))
            if q >= q_max:
                q = q_max
            if temp1 >= temp2:
                thc1 *= -1
            else:
                thc2 *= -1
            delta_t1 = q / thc1
            delta_t2 = q / thc2
            new_temp1 = temp1 + delta_t1
            new_temp2 = temp2 + delta_t2
            return new_temp1, new_temp2



        counter = 0
        time_passed = 0
        min_liquid_temp = 10000
        unchanged_count = 0

        while True:
                counter += 1
        # Calculating building contents ⇔ buildings     interactions
            # Calculating heat exchange between coolant/liquid and coolant/liquid pipe 
                for i in interact.values():
                    for j in i.keys():
                        q = TC_calcul_rpipe_pipecont(materials[j]["tc"], metal_tc, i[j]["temp"], i[j]["p_temp"])
                        i[j]["temp"], i[j]["p_temp"] = SHC_calcul(q, materials[j]["weight"], 50000, materials[j]["shc"],metal_shc, i[j]["temp"], i[j]["p_temp"])

        # Calculating building ⇔ tiles     interactions
            # Calculating heat exchange between coolant/liquid pipe and coolant/liquid tile
                for i in interact.values():
                    for j in i.keys():
                        q = TC_calcul_building_cell(metal_tc, metal_tc, i[j]["p_temp"], i[j]["t_temp"], 0.2, 1, 50000, 100000, metal_shc, metal_shc, 1, 1)
                        i[j]["p_temp"], i[j]["t_temp"] = SHC_calcul(q, 50000, 100000, metal_shc, metal_shc, i[j]["p_temp"], i[j]["t_temp"])
                                    
        # Calculating tile ⇔ tile      interactions
            # Calculating heat exchange between coolant tiles and liquid tiles
                for i in interact.values():
                    q = TC_calcul_solid_solid(metal_tc, metal_tc, i["liquid"]["t_temp"], i["coolant"]["t_temp"])
                    i["liquid"]["t_temp"], i["coolant"]["t_temp"] = SHC_calcul(q, 100000, 100000, metal_shc, metal_shc, i["liquid"]["t_temp"], i["coolant"]["t_temp"])

            # Calculating heat exchange between side-to-side interacts
                for i in list(interact.keys())[:-1]:
                    for j in interact[i].keys():
                        q = TC_calcul_solid_solid(metal_tc, metal_tc, interact[i][j]["t_temp"], interact[i+1][j]["t_temp"])
                        interact[i][j]["t_temp"], interact[i+1][j]["t_temp"] = SHC_calcul(q, 100000, 100000, metal_shc, metal_shc, interact[i][j]["t_temp"], interact[i+1][j]["t_temp"])



                if min_liquid_temp > round(interact[1]["liquid"]["temp"], 2):
                    min_liquid_temp = round(interact[1]["liquid"]["temp"], 2)
                    unchanged_count = 0
                else:
                    unchanged_count += 1
                    if unchanged_count >= 1000:
                        with open("results.txt", "a") as file:
                            file.write(
                            f"{coolant_temperature * 2},"
                            f"{interaction_number},"
                            f"{min_liquid_temp}\n"
                            )
                        break

                time_passed = round(time_passed + delta_t, 2)

                if round(time_passed, 2).is_integer():
            # Reassigning/resetting values
                    for i in list(interact.keys())[:-1]:
                        interact[i+1]["coolant"]["temp"] = interact[i]["coolant"]["temp"]
                        
                        interact[i]["liquid"]["temp"] = interact[i+1]["liquid"]["temp"]


                    interact[max(interact.keys())]["liquid"]["temp"] = liquid_temp

                    interact[1]["coolant"]["temp"] = coolant_temp


# For anyone wondering, all of this part is just held together with duct tape, I just stole everything from internet
# It's definitely not efficient, I am only good at doing what is above

data = np.loadtxt("results.txt", delimiter=",")

coolant_temp = data[:, 0]
interaction_count = data[:, 1]
min_liquid_temp = data[:, 2]

coolant_values = np.unique(coolant_temp)
interaction_values = np.unique(interaction_count)

X, Y = np.meshgrid(coolant_values, interaction_values)
Z = min_liquid_temp.reshape(len(coolant_values), len(interaction_values)).T
base = plt.get_cmap("coolwarm")

vmin = np.min(Z)
vmax = np.max(Z)

green_start = (Ideal_temperature_range_minimum - vmin) / (vmax - vmin)
green_end = (Ideal_temperature_range_maximum - vmin) / (vmax - vmin)
colors = base(np.linspace(0, 1, 256))

low = int(green_start * 255)
high = int(green_end * 255)

colors[low:high + 1] = [0, 1, 0, 1]

cmap = ListedColormap(colors)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
hover_text = ax.text2D(
    0.02, 0.95, "",
    transform=ax.transAxes,
    verticalalignment="top"
)
surface = ax.plot_surface(X, Y, Z, cmap=cmap, vmin=vmin, vmax=vmax)
fig.colorbar(surface, ax=ax, label="Minimum liquid temperature (°C)")
ax.set_xlabel("Coolant temperature (°C)")
ax.set_ylabel("Interaction count")
ax.set_zlabel("Reached liquid temperature (°C)")

def rotate(event):

    if event.key == "+":
        ax.view_init(elev=ax.elev, azim=ax.azim + 5)

    elif event.key == "-":
        ax.view_init(elev=ax.elev, azim=ax.azim - 5)

    fig.canvas.draw_idle()

def hover(event):
    if event.inaxes != ax:
        hover_text.set_text("")
        fig.canvas.draw_idle()
        return

    best_distance = float("inf")
    best_x = None
    best_y = None
    best_z = None

    for row in range(len(interaction_values)):
        for col in range(len(coolant_values)):
            x = X[row, col]
            y = Y[row, col]
            z = Z[row, col]

            x2, y2, _ = proj3d.proj_transform(
                x, y, z, ax.get_proj()
            )

            screen_x, screen_y = ax.transData.transform((x2, y2))

            distance = (
                (screen_x - event.x) ** 2
                + (screen_y - event.y) ** 2
            )

            if distance < best_distance:
                best_distance = distance
                best_x = x
                best_y = y
                best_z = z

    if True:
        hover_text.set_text(
            f"Coolant: {best_x:.0f} °C\n"
            f"Interactions: {best_y:.0f}\n"
            f"Minimum liquid: {best_z:.2f} °C"
        )


    fig.canvas.draw_idle()

fig.canvas.mpl_connect("key_press_event", rotate)
fig.canvas.mpl_connect("motion_notify_event", hover)


plt.show()