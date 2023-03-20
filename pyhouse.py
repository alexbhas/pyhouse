import streamlit as st
import requests
from bs4 import BeautifulSoup

def check_unique_title(soup):
    titles = soup.find_all('title')
    return len(titles) == 1

def check_html_lang(soup):
    html = soup.find('html')
    return 'lang' in html.attrs

def check_aria_roles(soup):
    elements_with_roles = soup.find_all(attrs={'role': True})
    return len(elements_with_roles)

def check_skip_navigation(soup):
    skip_links = soup.find_all(attrs={'href': lambda x: x and x.startswith('#')})
    return len(skip_links) > 0

def check_img_alt_tags(soup):
    images = soup.find_all('img')
    missing_alt = [img for img in images if not img.get('alt')]
    return len(missing_alt), len(images)

def check_heading_structure(soup):
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_levels = [int(h.name[1]) for h in headings]

    errors = 0
    for i in range(1, len(heading_levels)):
        if heading_levels[i] - heading_levels[i-1] > 1:
            errors += 1

    return errors, len(headings)

def analyze_web_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    unique_title = check_unique_title(soup)
    html_lang = check_html_lang(soup)
    aria_roles_count = check_aria_roles(soup)
    skip_navigation = check_skip_navigation(soup)
    missing_alt, total_images = check_img_alt_tags(soup)
    heading_errors, total_headings = check_heading_structure(soup)

    return {
        'unique_title': unique_title,
        'html_lang': html_lang,
        'aria_roles_count': aria_roles_count,
        'skip_navigation': skip_navigation,
        'missing_alt': (missing_alt, total_images),
        'heading_errors': (heading_errors, total_headings),
    }

def main():
    st.title("Web Accessibility Checker")

    url = st.text_input("Enter the URL of the web page you want to analyze:")

    if st.button("Analyze"):
        if url:
            st.write("Analyzing the web page...")
            results = analyze_web_page(url)

            st.subheader("Accessibility Report")

            st.write(f"Unique title tag: {results['unique_title']}")
            st.write(f"HTML lang attribute: {results['html_lang']}")

            st.write(f"Total elements with ARIA roles: {results['aria_roles_count']}")
            st.write(f"Skip navigation link: {results['skip_navigation']}")

            st.write(f"Total images: {results['missing_alt'][1]}")
            st.write(f"Images missing alt text: {results['missing_alt'][0]}")

            st.write(f"Total headings: {results['heading_errors'][1]}")
            st.write(f"Heading structure errors: {results['heading_errors'][0]}")

        else:
            st.warning("Please enter a URL to analyze.")

if __name__ == '__main__':
    main()
