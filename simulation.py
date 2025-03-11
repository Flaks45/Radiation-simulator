import csv
import json
import os

import matplotlib.pyplot as plt
import numpy as np

from element import Element


def save_simulation(element: Element, fig: plt.Figure, decay_counts: np.ndarray, n_theoretical: np.ndarray) -> None:
    """
    Guarda la simulació com una imatge en una carpeta específica per a l'element.

    Arguments:
        element (Element): Un objecte de la classe `Element` que conté la informació de l'element a simular.
        fig (plt.Figure): La figura de matplotlib que conté la gràfica de la simulació a guardar.
        decay_counts (np.ndarray): Array amb els valors de la desintegració simulada.
        n_theoretical (np.ndarray): Array amb els valors de la desintegració teòrica.

    Returns:
        None: La funció guarda la imatge de la gràfica en el directori corresponent.
    """
    # Crear la carpeta principal si no existeix
    dir_path = f'saved_simulations/{element.name}'
    os.makedirs(dir_path, exist_ok=True)

    # Buscar el següent índex disponible per guardar la gràfica
    existing_files = os.listdir(dir_path)
    next_index = len(existing_files) + 1

    # Crear la subcarpeta amb el número de l'índex
    subdir_path = os.path.join(dir_path, str(next_index))
    os.makedirs(subdir_path, exist_ok=True)

    # Guardar la gràfica com a imatge PNG dins la subcarpeta
    plot_filename = os.path.join(subdir_path, 'simulation.png')
    fig.savefig(plot_filename)

    # Crear les metadades
    metadata = {
        "name": element.name,
        "initial_atoms": element.n0,
        "half_life": element.half_life,
        "lambda_decay": element.lambda_decay,
        "precision": element.precision,
        "time_steps": element.time_steps
    }

    # Guardar les metadades com a fitxer JSON
    metadata_filename = os.path.join(subdir_path, 'metadata.json')
    with open(metadata_filename, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    # Guardar els valors de la simulació i la desintegració teòrica com a CSV
    csv_filename = os.path.join(subdir_path, 'simulation_data.csv')
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escriure els noms de les columnes
        writer.writerow(["Time Step", "Simulated Decay", "Theoretical Decay"])

        # Escriure les dades
        for t, (simulated, theoretical) in enumerate(zip(decay_counts, n_theoretical)):
            writer.writerow([t, simulated, theoretical])


def simulate(element: Element, *, show_plot: bool = True) -> dict[str: plt.Figure, str: np.ndarray, str: np.ndarray]:
    """
    Simula la desintegració radioactiva d'un element i compara els resultats simulats amb l'aproximació teòrica.

    La simulació segueix un model probabilístic on cada àtom té una probabilitat de desintegrar-se en cada pas de temps,
    amb una probabilitat de desintegració de P(λ). Els resultats es comparen amb l'equació teòrica N(t) = N₀·e^(−λ·t).

    Arguments:
        element (Element): Un objecte de la classe `Element` que conté la informació de l'element a simular.
        show_plot (bool, opcional): Ensenyar o no la gràfica un cop simulat.

    Returns:
        dict (str: plt.Figure, str: np.ndarray, str: np.ndarray): fig, decay_counts i n_theoretical.

    El gràfic mostrarà:
        - La desintegració simulada en temps discret.
        - L'aproximació teòrica de la desintegració.
        - La informació de l'element.
    """
    # Inicialització de paràmetres inicials
    n = element.n0
    decay_counts = np.zeros(element.time_steps, dtype=int)

    # Simulació de desintegració
    for t in range(0, element.time_steps, element.precision):
        # Si no hi ha àtoms
        if n <= 0:
            decay_counts[t:] = 0
            break  # Parar la simulació

        # Desintegrar àtoms a l'atzar
        decayed_atoms = np.sum(np.random.rand(n) < element.lambda_decay * element.precision)

        # Actualitzar les dades
        n -= decayed_atoms
        decay_counts[t:t + element.precision] = n

    # Aproximació teòrica de desintegració
    times = np.arange(element.time_steps)
    n_theoretical = element.n0 * np.exp(-element.lambda_decay * times)

    # Visualitzar els resultats
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(times, decay_counts, label="Desintegració Simulada", linestyle="solid", color="#FF0000")
    ax.plot(times, n_theoretical, label="Desintegració Teòrica N(T) = N₀·e^(−λ·t)", linestyle="dashed")

    ax.set_xlabel("Temps [s]")
    ax.set_ylabel("Àtoms Restants (N)")
    ax.set_title(f"Desintegració Radioactiva de {element.name}: Simulació vs. Aproximació Teòrica")
    ax.legend()

    # Afegir informació extra
    info_text = (
        f"Isòtop: {element.name}\n"
        f"Nombre d'àtoms inicials (N₀): {element.n0}\n"
        f"Nombre d'àtoms finals (N): {decay_counts[-1]}\n"
        f"Temps de semidesintegració (τ): {element.half_life:.2f} s\n"
        f"Constant de desintegració (λ): {element.format_lambda()} Bq\n"
        f"Temps total de simulació: {element.time_steps // 3600}h {(element.time_steps % 3600) // 60}m {element.time_steps % 60}s"
    )

    # Ensenyar la informació extra
    ax.annotate(
        info_text,
        xy=(0.99, 0.85),
        xycoords='axes fraction',
        fontsize=10,
        ha="right",
        va="top",
        bbox=dict(facecolor='white', edgecolor='#cccccc', boxstyle="round,pad=0.2", alpha=0.85)
    )

    # Guardar la simulació a ./saved_simulation/
    save_simulation(element, fig, decay_counts, n_theoretical)

    # Ensenyar la gràfica
    if show_plot:
        plt.show()

    # Retornar els resultats de la simulació
    return {
        "fig": fig,
        "decay_counts": decay_counts,
        "n_theoretical": n_theoretical
    }
