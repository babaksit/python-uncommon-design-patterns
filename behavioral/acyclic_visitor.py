class GraphicElement:
    """
    Abstract base class for graphic elements.

    Methods
    -------
    accept(visitor)
        Accepts a visitor that performs an operation on the element.
    """
    def accept(self, visitor):
        pass


class Circle(GraphicElement):
    """
    Concrete class representing a circle element.

    Attributes
    ----------
    radius : float
        The radius of the circle.

    Methods
    -------
    accept(visitor)
        Accepts a visitor that performs an operation on the circle.
    """
    def __init__(self, radius):
        self.radius = radius

    def accept(self, visitor):
        if isinstance(visitor, CircleVisitor):
            visitor.visit_circle(self)


class Square(GraphicElement):
    """
    Concrete class representing a square element.

    Attributes
    ----------
    side : float
        The side length of the square.

    Methods
    -------
    accept(visitor)
        Accepts a visitor that performs an operation on the square.
    """
    def __init__(self, side):
        self.side = side

    def accept(self, visitor):
        if isinstance(visitor, SquareVisitor):
            visitor.visit_square(self)


class Triangle(GraphicElement):
    """
    Concrete class representing a triangle element.

    Attributes
    ----------
    base : float
        The base length of the triangle.
    height : float
        The height of the triangle.

    Methods
    -------
    accept(visitor)
        Accepts a visitor that performs an operation on the triangle.
    """
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def accept(self, visitor):
        if isinstance(visitor, TriangleVisitor):
            visitor.visit_triangle(self)
class CircleVisitor:
    """
    Interface for visitors that can visit a Circle.

    Methods
    -------
    visit_circle(circle)
        Visits a circle element.
    """
    def visit_circle(self, circle):
        pass


class SquareVisitor:
    """
    Interface for visitors that can visit a Square.

    Methods
    -------
    visit_square(square)
        Visits a square element.
    """
    def visit_square(self, square):
        pass


class TriangleVisitor:
    """
    Interface for visitors that can visit a Triangle.

    Methods
    -------
    visit_triangle(triangle)
        Visits a triangle element.
    """
    def visit_triangle(self, triangle):
        pass
class RenderVisitor(CircleVisitor, SquareVisitor, TriangleVisitor):
    """
    Concrete visitor for rendering graphic elements.

    Methods
    -------
    visit_circle(circle)
        Renders a circle.
    visit_square(square)
        Renders a square.
    visit_triangle(triangle)
        Renders a triangle.
    """

    def visit_circle(self, circle):
        print(f"Rendering a circle with radius {circle.radius}.")

    def visit_square(self, square):
        print(f"Rendering a square with side {square.side}.")

    def visit_triangle(self, triangle):
        print(f"Rendering a triangle with base {triangle.base} and height {triangle.height}.")


class AreaCalculationVisitor(CircleVisitor, SquareVisitor, TriangleVisitor):
    """
    Concrete visitor for calculating the area of graphic elements.

    Methods
    -------
    visit_circle(circle)
        Calculates the area of a circle.
    visit_square(square)
        Calculates the area of a square.
    visit_triangle(triangle)
        Calculates the area of a triangle.
    """

    def visit_circle(self, circle):
        area = 3.14159 * (circle.radius ** 2)
        print(f"Area of the circle: {area:.2f}")

    def visit_square(self, square):
        area = square.side ** 2
        print(f"Area of the square: {area:.2f}")

    def visit_triangle(self, triangle):
        area = 0.5 * triangle.base * triangle.height
        print(f"Area of the triangle: {area:.2f}")
        
if __name__ == "__main__":
    # Create some graphic elements
    circle = Circle(radius=5)
    square = Square(side=4)
    triangle = Triangle(base=3, height=6)

    # Create visitors
    render_visitor = RenderVisitor()
    area_visitor = AreaCalculationVisitor()

    # Apply the RenderVisitor
    print("Rendering elements:")
    circle.accept(render_visitor)
    square.accept(render_visitor)
    triangle.accept(render_visitor)

    # Apply the AreaCalculationVisitor
    print("\nCalculating areas:")
    circle.accept(area_visitor)
    square.accept(area_visitor)
    triangle.accept(area_visitor)