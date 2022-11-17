import time

import numpy as np



class Utils:
    @staticmethod
    def clean_string(row: str):
        if isinstance(row, str):
            return row.replace(".", "").strip()
        else:
            return row

    @staticmethod
    def delay(mean=0.5):
        """
        retourne un chiffre aléatoire suivant une distribution normal de moyenne 4 secondes et d'ecart-type de 0.8
        Ce chiffre aléatoire est le délai après chaque clique. Le but est de simuler le comportement d'un humain :
        un délai fixe peut attirer l'attention des contrôleurs, tout comme un délai aléatoire d'une distribution
        uniforme
        """
        bottom_mean_limit = 0.1
        assert mean >= bottom_mean_limit, f"{mean} needs to be >= {bottom_mean_limit}"
        sigma = mean * 0.2
        mini = sigma * 2
        delai = np.random.normal(mean, sigma, 1)[0]
        while delai < mini:
            delai = abs(np.random.normal(mean, sigma, 1)[0])
        time.sleep(delai)
