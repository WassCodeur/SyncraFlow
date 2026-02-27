from nanoid import generate
from slugify import slugify


def generat_slug(name):
    """Generate a unique slug for a workflow

    Args:
        name (str): The name of the workflow
    Returns:
        str: A unique slug for the workflow
    """
    slug = slugify(name) + '-' + generate(size=8)

    return slug


if __name__ == "__main__":
    print(generat_slug("My Workflow"))
