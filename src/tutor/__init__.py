"""
Primaclaw Krav Masa Self-Defense Tutor
Runs via the Primaclaw swarm or local Ollama.

Philosophy:
- Krav Maga: "Contact combat" — no-nonsense self-defense (IDF origin)
- Tactical awareness: CIA-style situational awareness, threat assessment
- Moral framework: "Blessed are the peacemakers" — avoid conflict when possible,
  but defend yourself and others when necessary (Luke 22:36, David vs Goliath)
"""

SYSTEM_PROMPT = """You are a Krav Masa self-defense instructor.

Krav Maga: Israeli self-defense. Neutralize threats fast. Simultaneous defense and attack. Target vulnerable areas (eyes, throat, groin, knees). Ground survival: get up fast. Never grapple on the ground.

Tactical awareness (CIA training): Cooper's Color Code (White/Yellow/Orange/Red/Black). OODA Loop (Observe, Orient, Decide, Act). Always know 2 escape routes. Watch for pre-attack indicators: pacing, target glancing, blading stance.

Moral framework: De-escalate first always. Use minimum force needed. Defend yourself and others. Preparation is wisdom, not aggression.

Teaching: Be direct and practical. Step-by-step instructions. Emphasize de-escalation. Teach self-defense only, never aggression. Every technique assumes you tried to leave first."""

# Training program levels
TRAINING_LEVELS = {
    "white": {
        "name": "White Belt — Awareness",
        "focus": "Situational awareness, basic stances, escape",
        "exercises": [
            "Practice Cooper's Color Code in daily life",
            "Escape drill: practice breaking grips on wrists",
            "360° defense: block circular attacks from all angles",
            "Verbal de-escalation scenarios",
        ],
    },
    "yellow": {
        "name": "Yellow Belt — Combatives",
        "focus": "Palm strikes, knee strikes, elbows",
        "exercises": [
            "Straight palm strike (chin/nose target)",
            "Knee strike to groin (clinch entry)",
            "Elbow strikes: horizontal, upward, downward",
            "Combination: palm → knee → push away → escape",
        ],
    },
    "orange": {
        "name": "Orange Belt — Ground & Chokes",
        "focus": "Ground survival, choke defenses",
        "exercises": [
            "Ground get-up (kick and stand — never grapple)",
            "Front choke defense: pluck + knee strike",
            "Rear choke defense: chin tuck + turn + strike",
            "Headlock defense: base → body strike → escape",
        ],
    },
    "green": {
        "name": "Green Belt — Weapons",
        "focus": "Weapon awareness, basic disarms",
        "exercises": [
            "Knife threat defense (redirect + control + disarm)",
            "Stick/bat defense (close distance → inside)",
            "Gun threat: side disarm (redirect barrel + control)",
            "ALWAYS: give up belongings first. Money < life.",
        ],
    },
    "blue": {
        "name": "Blue Belt — Multiple Attackers",
        "focus": "Positioning, funneling, escape priority",
        "exercises": [
            "Line drill: keep attackers in front of you",
            "Use one attacker as shield",
            "Never go to the ground with multiple attackers",
            "Escape is always the primary goal",
        ],
    },
}


def get_training_plan(level="white"):
    """Return training plan for a given level."""
    return TRAINING_LEVELS.get(level, TRAINING_LEVELS["white"])
