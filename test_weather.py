import os
from playwright.sync_api import sync_playwright

def test_weather_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        html_path = os.path.abspath("index.html")
        page.goto(f"file://{html_path}")
        
        # 1. Verificar carga inicial (Stockholm)
        assert "Stockholm" in page.locator("#city-name").inner_text()
        print("✅ Carga inicial correcta: Stockholm")
        
        # 2. Probar búsqueda de otra ciudad (Madrid)
        page.fill("#city-input", "Madrid")
        page.click("button")
        
        assert "Madrid" in page.locator("#city-name").inner_text()
        assert "18°C" in page.locator("#temp-value").inner_text()
        print("✅ Búsqueda exitosa: Madrid (18°C)")
        
        # 3. Probar manejo de errores (ciudad inexistente)
        page.fill("#city-input", "CiudadInventada")
        page.click("button")
        assert page.locator("#error").is_visible()
        print("✅ Manejo de errores verificado correctamente.")
        
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    test_weather_app()