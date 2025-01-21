from create_technical_diagrams import (
    create_vertical_projection,
    create_horizontal_projection,
    create_construction_details
)

def main():
    print('Generating vertical projection...')
    create_vertical_projection()

    print('Generating horizontal projection...')
    create_horizontal_projection()

    print('Generating construction details...')
    create_construction_details()

    print('All drawings generated successfully.')

if __name__ == "__main__":
    main()
