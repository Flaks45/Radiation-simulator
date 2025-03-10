import numpy as np


class Element:
    """
    Informació d'un element que experimenta una desintegració radioactiva.

    Attributes:
        name (str): Nom de l'element.
        N0 (int): Nombre inicial d'àtoms o partícules de l'element.
        half_life (float, opcional): Temps de semidesintegració en segons. Necessari si no es proporciona la constant de desintegració.
        lambda_decay (float, opcional): Constant de desintegració. Necessària si no es proporciona el temps de semidesintegració.
        time_steps (int, opcional): Temps de simulació. Per defecte 1 hora = 3600s.
        precision (int, opcional): Segons per pas de simulació. Per defecte 1s.
    """

    def __init__(self, name: str, N0: int, half_life: float = None, lambda_decay: float = None,
                 time_steps: int = 3600, precision: int = 1):
        self.name = name
        self.N0 = N0
        self.time_steps = time_steps
        self.precision = precision

        if time_steps % precision:
            raise ValueError("Per favor, utilitza una precisió múltiple del temps de simulació.")

        # Calcular temps de semidesintegració o constant de desintegració
        if half_life is None and lambda_decay is None:
            raise ValueError("Introdueix el temps de semidesintegració o la constant de desintegració.")
        elif half_life is None:
            self.lambda_decay = lambda_decay
            self.lambda_decay = np.log(2) / lambda_decay
        elif lambda_decay is None:
            self.half_life = half_life
            self.lambda_decay = np.log(2) / half_life

    def format_lambda(self) -> str:
        """
        Dona la constant de desintegració en notació científica.

        Returns:
            str: La constant de desintegració com una cadena de text en notació científica.
        """
        lambda_mantissa, lambda_exponent = f"{self.lambda_decay:.4e}".split("e")
        return f"{lambda_mantissa}·10^({int(lambda_exponent)})"
