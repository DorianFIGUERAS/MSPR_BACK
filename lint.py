import subprocess
import sys

# Configuration de flake8
config = {
    "ignore": "E203, E266, E501, W503, W291, E305, E211, E265, W191",
    "max-complexity": 10,
    "max-line-length": 88,
}

# Construire la commande flake8
command = [
    "flake8",
    ".",
    f"--ignore={config['ignore']}",
    f"--max-complexity={config['max-complexity']}",
    f"--max-line-length={config['max-line-length']}",
]

# Exécuter la commande
result = subprocess.run(command, capture_output=True, text=True)

# Afficher le résultat
print(result.stdout)
print(result.stderr, file=sys.stderr)

# Sortie avec le code de sortie de flake8
sys.exit(result.returncode)
