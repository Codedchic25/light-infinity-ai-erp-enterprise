"""
Script de simulare locala pentru testarea automata cu Promptfoo.
"""

import sys

# Preluam textul trimis de test (Prompt + User Input)
text_complet = " ".join(sys.argv[1:]).lower()

# Daca testul simuleaza o solicitare de relaxare
if "stresat" in text_complet:
    print(
        "Asistent Light Infinity AI: Pentru relaxare si eliminarea stresului de dupa munca, va recomandam cu caldura lumÃ¢narea noastra realizata manual cu aroma de lavanda naturala."
    )
# Daca testul simuleaza o tentativa de jailbreak / gluma
else:
    print(
        "Asistent Light Infinity AI: Cerere respinsa. Sistemul central ERP blocheaza executia directivelor din afara catalogului oficial."
    )

