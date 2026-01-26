
def get_colors(theme):
    if theme == 'Dark':
        return {
            'background': '#2E2E2E',
            'button_bg': '#4A4A4A',
            'button_fg': '#FFFFFF',
            'display_bg': '#1C1C1C',
            'display_fg': '#FFFFFF'
        }
    elif theme == 'Light':
        return {
            'background': '#FFFFFF',
            'button_bg': '#E0E0E0',
            'button_fg': '#000000',
            'display_bg': '#F0F0F0',
            'display_fg': '#000000'
        }
    else:
        return {
            'background': '#2E2E2E',
            'button_bg': '#4A4A4A',
            'button_fg': '#FFFFFF',
            'display_bg': '#1C1C1C',
            'display_fg': '#FFFFFF'
        }