# Adapter Pattern

## Problem Statement
- Convert the **interface of a class into another interface** that clients expect.
- Allow classes with **incompatible interfaces** to work together without modifying their source code.
- Wrap a legacy or third-party API so it conforms to the interface your application expects.

**Example inputs/outputs:**
- `adapter.request()` → internally calls `legacyService.specificRequest()` and transforms the result
- `adapter.getData()` → adapts XML response from legacy system into JSON format expected by the client

**Edge cases:**
- Adapting an interface with more methods than the target (partial adaptation)
- Adapting an interface with fewer methods (may need default behavior)
- Handling errors from the adaptee that don't map to the target interface
- Adapting asynchronous APIs to synchronous interfaces (or vice versa)

## Solutions

### Solution 1: Object Adapter (Composition)
- **Time Complexity:** O(1) for delegation; depends on the adaptee's method
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod
import json


class ModernWeatherService(ABC):
    """Interface the application expects."""
    @abstractmethod
    def get_temperature(self, city: str) -> dict:
        pass

    @abstractmethod
    def get_forecast(self, city: str, days: int) -> dict:
        pass


class LegacyWeatherAPI:
    """Old third-party API with a different interface."""
    def fetch_weather_xml(self, city_code: str) -> str:
        return f"<weather><city>{city_code}</city><temp>72</temp><unit>F</unit></weather>"

    def fetch_forecast_xml(self, city_code: str, num_days: int) -> str:
        forecasts = "".join(
            f"<day><n>{i+1}</n><temp>{70+i}</temp></day>"
            for i in range(num_days)
        )
        return f"<forecast><city>{city_code}</city>{forecasts}</forecast>"


class WeatherAdapter(ModernWeatherService):
    """Adapts LegacyWeatherAPI to ModernWeatherService interface."""
    CITY_MAP = {"New York": "NYC", "London": "LDN", "Tokyo": "TKY"}

    def __init__(self, legacy_api: LegacyWeatherAPI):
        self._api = legacy_api

    def _resolve_city_code(self, city: str) -> str:
        code = self.CITY_MAP.get(city)
        if code is None:
            raise ValueError(f"Unknown city: {city}")
        return code

    def get_temperature(self, city: str) -> dict:
        code = self._resolve_city_code(city)
        xml = self._api.fetch_weather_xml(code)
        temp = int(xml.split("<temp>")[1].split("</temp>")[0])
        unit = xml.split("<unit>")[1].split("</unit>")[0]
        celsius = round((temp - 32) * 5 / 9, 1) if unit == "F" else temp
        return {"city": city, "temperature": celsius, "unit": "C"}

    def get_forecast(self, city: str, days: int) -> dict:
        code = self._resolve_city_code(city)
        xml = self._api.fetch_forecast_xml(code, days)
        forecasts = []
        for part in xml.split("<day>")[1:]:
            day_num = int(part.split("<n>")[1].split("</n>")[0])
            temp_f = int(part.split("<temp>")[1].split("</temp>")[0])
            temp_c = round((temp_f - 32) * 5 / 9, 1)
            forecasts.append({"day": day_num, "temperature": temp_c, "unit": "C"})
        return {"city": city, "forecast": forecasts}


# Usage
legacy = LegacyWeatherAPI()
weather = WeatherAdapter(legacy)

print(json.dumps(weather.get_temperature("New York"), indent=2))
# {"city": "New York", "temperature": 22.2, "unit": "C"}

print(json.dumps(weather.get_forecast("London", 3), indent=2))
# {"city": "London", "forecast": [{"day": 1, ...}, ...]}
```

#### JavaScript
```javascript
class LegacyWeatherAPI {
  fetchWeatherXml(cityCode) {
    return `<weather><city>${cityCode}</city><temp>72</temp><unit>F</unit></weather>`;
  }

  fetchForecastXml(cityCode, numDays) {
    const forecasts = Array.from({ length: numDays }, (_, i) =>
      `<day><n>${i + 1}</n><temp>${70 + i}</temp></day>`
    ).join("");
    return `<forecast><city>${cityCode}</city>${forecasts}</forecast>`;
  }
}

class WeatherAdapter {
  static #CITY_MAP = { "New York": "NYC", "London": "LDN", "Tokyo": "TKY" };

  constructor(legacyApi) {
    this.api = legacyApi;
  }

  #resolveCityCode(city) {
    const code = WeatherAdapter.#CITY_MAP[city];
    if (!code) throw new Error(`Unknown city: ${city}`);
    return code;
  }

  getTemperature(city) {
    const code = this.#resolveCityCode(city);
    const xml = this.api.fetchWeatherXml(code);
    const temp = parseInt(xml.match(/<temp>(\d+)<\/temp>/)[1]);
    const unit = xml.match(/<unit>(\w)<\/unit>/)[1];
    const celsius = unit === "F"
      ? Math.round(((temp - 32) * 5) / 9 * 10) / 10
      : temp;
    return { city, temperature: celsius, unit: "C" };
  }

  getForecast(city, days) {
    const code = this.#resolveCityCode(city);
    const xml = this.api.fetchForecastXml(code, days);
    const forecasts = [...xml.matchAll(/<day><n>(\d+)<\/n><temp>(\d+)<\/temp><\/day>/g)]
      .map(match => ({
        day: parseInt(match[1]),
        temperature: Math.round(((parseInt(match[2]) - 32) * 5) / 9 * 10) / 10,
        unit: "C",
      }));
    return { city, forecast: forecasts };
  }
}

// Usage
const legacy = new LegacyWeatherAPI();
const weather = new WeatherAdapter(legacy);

console.log(weather.getTemperature("New York"));
// { city: 'New York', temperature: 22.2, unit: 'C' }

console.log(weather.getForecast("London", 3));
// { city: 'London', forecast: [{ day: 1, ... }, ...] }
```

#### Java
```java
import java.util.*;
import java.util.regex.*;

// ModernWeatherService.java
public interface ModernWeatherService {
    Map<String, Object> getTemperature(String city);
    Map<String, Object> getForecast(String city, int days);
}

// LegacyWeatherAPI.java
public class LegacyWeatherAPI {
    public String fetchWeatherXml(String cityCode) {
        return "<weather><city>" + cityCode
            + "</city><temp>72</temp><unit>F</unit></weather>";
    }

    public String fetchForecastXml(String cityCode, int numDays) {
        StringBuilder sb = new StringBuilder();
        sb.append("<forecast><city>").append(cityCode).append("</city>");
        for (int i = 0; i < numDays; i++) {
            sb.append("<day><n>").append(i + 1)
              .append("</n><temp>").append(70 + i)
              .append("</temp></day>");
        }
        sb.append("</forecast>");
        return sb.toString();
    }
}

// WeatherAdapter.java
public class WeatherAdapter implements ModernWeatherService {
    private static final Map<String, String> CITY_MAP = Map.of(
        "New York", "NYC", "London", "LDN", "Tokyo", "TKY"
    );
    private final LegacyWeatherAPI api;

    public WeatherAdapter(LegacyWeatherAPI api) {
        this.api = api;
    }

    private String resolveCityCode(String city) {
        String code = CITY_MAP.get(city);
        if (code == null) {
            throw new IllegalArgumentException("Unknown city: " + city);
        }
        return code;
    }

    @Override
    public Map<String, Object> getTemperature(String city) {
        String code = resolveCityCode(city);
        String xml = api.fetchWeatherXml(code);

        Matcher tempMatcher = Pattern.compile("<temp>(\\d+)</temp>").matcher(xml);
        Matcher unitMatcher = Pattern.compile("<unit>(\\w)</unit>").matcher(xml);
        tempMatcher.find();
        unitMatcher.find();

        int temp = Integer.parseInt(tempMatcher.group(1));
        String unit = unitMatcher.group(1);
        double celsius = unit.equals("F")
            ? Math.round((temp - 32) * 5.0 / 9.0 * 10) / 10.0
            : temp;

        return Map.of("city", city, "temperature", celsius, "unit", "C");
    }

    @Override
    public Map<String, Object> getForecast(String city, int days) {
        String code = resolveCityCode(city);
        String xml = api.fetchForecastXml(code, days);

        List<Map<String, Object>> forecasts = new ArrayList<>();
        Matcher m = Pattern.compile(
            "<day><n>(\\d+)</n><temp>(\\d+)</temp></day>"
        ).matcher(xml);

        while (m.find()) {
            int dayNum = Integer.parseInt(m.group(1));
            int tempF = Integer.parseInt(m.group(2));
            double tempC = Math.round((tempF - 32) * 5.0 / 9.0 * 10) / 10.0;
            forecasts.add(Map.of(
                "day", dayNum, "temperature", tempC, "unit", "C"
            ));
        }
        return Map.of("city", city, "forecast", forecasts);
    }
}

// Usage
// LegacyWeatherAPI legacy = new LegacyWeatherAPI();
// ModernWeatherService weather = new WeatherAdapter(legacy);
// System.out.println(weather.getTemperature("New York"));
// Output: {city=New York, temperature=22.2, unit=C}
```

**Explanation:** The Object Adapter uses composition — it holds a reference to the legacy API and translates calls from the modern interface to the legacy interface. The `WeatherAdapter` wraps `LegacyWeatherAPI`, translating city names to city codes, parsing XML responses, and converting Fahrenheit to Celsius. The client code works exclusively with the `ModernWeatherService` interface, unaware that a legacy system is behind it. This is the most common adapter variant because it doesn't require inheritance from the adaptee.

**When to use:** When integrating legacy systems, third-party libraries, or external APIs that don't match your application's expected interface. The most common scenario in real-world software engineering.

### Solution 2: Class Adapter (Multiple Inheritance)
- **Time Complexity:** O(1) for delegation
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod


class TargetInterface(ABC):
    @abstractmethod
    def process(self, data: dict) -> str:
        pass


class LegacyProcessor:
    """Legacy class with an incompatible interface."""
    def legacy_process(self, raw_string: str) -> str:
        return raw_string.upper()


class ProcessorAdapter(TargetInterface, LegacyProcessor):
    """Class adapter using multiple inheritance."""
    def process(self, data: dict) -> str:
        raw = str(data)
        return self.legacy_process(raw)


# Usage
adapter = ProcessorAdapter()
result = adapter.process({"key": "value"})
print(result)  # {'KEY': 'VALUE'}
```

#### JavaScript
```javascript
// JavaScript doesn't support multiple inheritance, so class adapters
// are typically implemented using mixins or composition. Here's a
// mixin-based approach:

const LegacyProcessor = (Base) =>
  class extends Base {
    legacyProcess(rawString) {
      return rawString.toUpperCase();
    }
  };

class BaseAdapter {
  process(data) {
    throw new Error("Subclasses must implement process()");
  }
}

class ProcessorAdapter extends LegacyProcessor(BaseAdapter) {
  process(data) {
    const raw = JSON.stringify(data);
    return this.legacyProcess(raw);
  }
}

// Usage
const adapter = new ProcessorAdapter();
console.log(adapter.process({ key: "value" }));
// {"KEY":"VALUE"}
```

#### Java
```java
// Java doesn't support multiple class inheritance. Use interface
// inheritance combined with extending the adaptee class:

// TargetInterface.java
public interface TargetInterface {
    String process(Map<String, Object> data);
}

// LegacyProcessor.java
public class LegacyProcessor {
    public String legacyProcess(String rawString) {
        return rawString.toUpperCase();
    }
}

// ProcessorAdapter.java
public class ProcessorAdapter extends LegacyProcessor implements TargetInterface {
    @Override
    public String process(Map<String, Object> data) {
        String raw = data.toString();
        return legacyProcess(raw);
    }
}

// Usage
// TargetInterface adapter = new ProcessorAdapter();
// String result = adapter.process(Map.of("key", "value"));
// System.out.println(result); // {KEY=VALUE}
```

**Explanation:** The Class Adapter uses inheritance — it extends the adaptee class and implements the target interface simultaneously. The adapter inherits the legacy behavior directly and overrides/implements the target methods. This approach is more limited than the Object Adapter: it can only adapt a single class (not a class hierarchy), and it tightly couples the adapter to the adaptee. Python supports this natively via multiple inheritance. Java and JavaScript approximate it through interface implementation combined with class extension or mixins.

**When to use:** When you need direct access to the adaptee's protected members, or when the adaptee has many methods and you want to inherit most of them unchanged. Less common than the Object Adapter in practice due to its coupling limitations.

## Variations & Extensions
- **Two-Way Adapter:** Implements both interfaces, allowing the adapter to be used as either type
- **Default Adapter (Stub):** Provides no-op implementations for all methods of a large interface, letting subclasses override only the methods they care about
- **Async Adapter:** Wraps a synchronous API to provide an async interface (or vice versa)
- **Facade vs. Adapter:** A facade simplifies a complex subsystem; an adapter makes an incompatible interface compatible — they can be combined

## Real-World Applications
- Database ORM layers adapting SQL dialects to a unified API
- Logging framework adapters (SLF4J adapting Log4j, Logback, JUL)
- Payment gateway integrations — adapting Stripe, PayPal, and Square to a common `PaymentProcessor` interface
- File format converters — adapting CSV, XML, or Parquet readers to a common `DataSource` interface
- Cloud SDK wrappers — adapting AWS, GCP, and Azure APIs to a unified cloud abstraction

## Tags
#design-pattern #structural #adapter #wrapper #integration #medium
