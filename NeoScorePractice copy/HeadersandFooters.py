from neoscore.common import *
import pathlib

neoscore.setup()

# Use a smaller paper for doc example
neoscore.document.paper = Paper(Mm(200), Mm(150), Mm(10), Mm(10), Mm(10), Mm(10))

# # adds a custom overlay to all new pages
# def overlay(page: Page):
#     page_rect = page.bounding_rect
#     # Draw a rectangle around the entire page
#     Path.rect((page_rect.x, page_rect.y), page,
#         page_rect.width, page_rect.height, Brush.no_brush())
#     # And write some text
#     Text(ORIGIN, page, f"some overlay text on page {page.index + 1}")

# neoscore.document.pages.overlay_func = overlay

# Since the first page is a right-side page, corner text will appear on the right edge
neoscore.document.pages.overlay_func = simple_header_footer(
    "outside top - Page %page",
    "centered top",
    "outside bottom",
    "centered bottom",
)

Text((Mm(50), Mm(50)), None, "text directly on the page")


# Creating new pages and adding content to them

first_page = neoscore.document.pages[0]

second_page = neoscore.document.pages[1]

Text((Mm(50), Mm(70)), second_page, "New page content")

neoscore.render_pdf("/Users/maver/Downloads/my_document.pdf", 300)

neoscore.show()