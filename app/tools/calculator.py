import logging
import sympy

logger = logging.getLogger(__name__)


def calculate(expression: str) -> str:
    try:
        result = sympy.sympify(expression)
        return str(result)
    except Exception as e:
        logger.warning(f"Invalid expression: '{expression}' | error: {e}")
        return "Could not evaluate the expression."