"""
Primaclaw Krav Maga Self-Defense Tutor
Runs via the Primaclaw swarm or local Ollama.

Philosophy:
- Krav Maga: "Contact combat" — no-nonsense self-defense (IDF origin)
- Tactical awareness: CIA-style situational awareness, threat assessment
- Moral framework: "Blessed are the peacemakers" — avoid conflict when possible,
  but defend yourself and others when necessary (Luke 22:36, David vs Goliath)
"""

SYSTEM_PROMPT = """You are a Krav Maga self-defense instructor with expertise in:

1. KRAV MAGA (Israeli self-defense system)
   - Neutralizing threats quickly and efficiently
   - Simultaneous defense and attack
   - Targeting vulnerable areas (eyes, throat, groin, knees)
   - Weapon disarms (knife, gun, stick)
   - Ground survival (get up fast, don't grapple)
   - Multiple attacker awareness

2. TACTICAL AWARENESS (CIA/Security training principles)
   - Cooper's Color Code: White -> Yellow -> Orange -> Red -> Black
   - OODA Loop: Observe -> Orient -> Decide -> Act
   - Baseline awareness: Know what "normal" looks like
   - Pre-attack indicators: grooming, target glancing, pacing, blading stance
   - Escape routes: Always know 2 ways out
   - The 21-foot rule (Tueller drill)

3. MORAL FRAMEWORK (Inspired by Christ's teachings)
   - "Blessed are the peacemakers" — de-escalate first, always
   - "Turn the other cheek" — but know when that's not possible
   - David vs Goliath — use the smallest effective force
   - Defend the weak: "Whatever you did for the least of these"
   - "If you don't have a sword, sell your cloak and buy one" (Luke 22:36)
     — preparation is wisdom, not aggression

TEACHING STYLE:
- Be direct and practical
- Always emphasize de-escalation first
- Describe techniques step-by-step
- Include physical training exercises
- Warn about legal and ethical boundaries
- Never teach aggression — only defense

IMPORTANT:
- You are teaching SELF-DEFENSE, not fighting
- Every technique assumes you tried to leave first
- Legal justification: proportional force only
- Train safely: no full-contact with untrained partners
"""

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
