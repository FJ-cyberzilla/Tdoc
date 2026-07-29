TDOC Doctor - Test Enhancement Plan (Current State)

📊 Current Coverage Summary

· Overall: ~95% A-rated
· A-Rated Methods: 270+ items (excellent)
· B-Rated Methods: 4 items
· C-Rated Methods: 4 items

---

🔴 CRITICAL - C-Rated Methods (Fix Immediately)

1. src/services/network/sms.py

· Method: SMSChecker.check (C)
· Why C-Rated:
  · Complex Android SMS database queries
  · Multiple failure points (permissions, API availability)
  · Fallback logic paths
  · SIM state dependencies
  · Content provider interactions

Test Cases Needed:

· Termux API available → returns SMS count
· Termux API fails → fallback to content provider
· Content provider accessible → returns SMS data
· Content provider permission denied → graceful failure
· No SIM card → returns 0 SMS
· Empty inbox → returns 0 count
· SMS database corrupted → error handling
· Android version differences (API levels)
· Mock ContentResolver queries
· Test Cursor parsing
· Verify SMS count accuracy
· Test read/unread status detection

2. src/ui/renderers/renderer.py

· Method: UIRenderer.render_network_metrics (C)
· Why C-Rated:
  · 249 lines long (too complex)
  · Multiple network components (WiFi, VPN, Telephony, DNS)
  · Visual rendering logic
  · Color coding based on values
  · Grid layout management

Refactoring + Test Plan:

· Split into 5 smaller methods:
  1. _render_wifi_panel - WiFi SSID, signal, speed
  2. _render_vpn_panel - VPN status, type, IP
  3. _render_telephony_panel - Carrier, signal, network type
  4. _render_dns_panel - DNS servers, resolution time
  5. _render_network_health - Latency, packet loss

Test Cases:

· All network data present → full display
· Missing WiFi → show "Not Connected"
· Missing VPN → hide VPN panel
· Telephony data null → show "No SIM"
· Signal strength range testing (-30 to -120 dBm)
· Color thresholds: excellent/good/fair/poor
· Responsive layout with different terminal widths
· Unicode glyphs rendering correctly
· Null values handling
· Partial data display

3. src/ui/models/network.py

· Method: TelephonyModel.from_dict (C)
· Why C-Rated:
  · Complex telephony data parsing
  · Multiple nullable fields
  · Network type normalization
  · Operator name extraction

Test Cases:

· Complete data → all fields populated
· Missing operator name → empty string
· Invalid network type → "Unknown"
· Signal strength normalization (ASU to dBm)
· Roaming status parsing
· SIM state detection
· Data connectivity status
· Network capabilities parsing
· IMS registration status
· VoLTE/VoWiFi detection

---

🟡 HIGH - B-Rated Methods

4. src/ui/renderers/renderer.py

· Method: UIRenderer._format_signal_strength (B)

Test Cases:

· -30 dBm → Excellent (5 bars, green)
· -50 dBm → Good (4 bars, light green)
· -65 dBm → Fair (3 bars, yellow)
· -80 dBm → Poor (2 bars, orange)
· -100 dBm → Weak (1 bar, red)
· -999 dBm → No signal
· 0 dBm → Default/unknown
· -150 dBm → Edge case
· Invalid input → graceful handling

5. src/services/network/wifi.py

· Method: WifiChecker.check (B)

Test Cases:

· WiFi enabled, connected → return SSID, signal, speed
· WiFi disabled → return disabled state
· Termux API available → use API
· Termux API unavailable → fallback to iwconfig
· Hidden SSID → return "Hidden Network"
· No WiFi hardware → return "Not Available"
· Scanning in progress → return scanning state
· WPA3 security detection
· WiFi 6 (802.11ax) detection
· 5GHz band detection
· Connection speed in Mbps
· Channel number parsing

6. src/services/network/hotspot.py

· Method: HotspotChecker.check (B)

Test Cases:

· Hotspot enabled → return active state
· Hotspot disabled → return inactive
· Connected clients → count and MAC addresses
· No connected clients → 0 count
· SSID broadcasting on/off
· Security type (Open/WPA2/WPA3)
· Password set/empty
· Band (2.4GHz/5GHz)
· Device limitations (Android specific)
· API permission denied
· Root vs non-root detection

7. src/services/environment/sensors.py

· Method: SensorCollector.get_sensor_data (B)

Test Cases:

· All sensors available → full data
· Thermal zone sensors → temperature readings
· Accelerometer → X,Y,Z values
· Gyroscope → rotation data
· Light sensor → lux values
· Proximity sensor → distance
· Sensor permission denied → partial data
· No sensors → empty result
· Sensor reading timeout
· Battery temperature sensor
· CPU temperature via thermal zones
· Sensor sampling rates
· Data normalization

---

🟢 MEDIUM - Edge Cases for A-Rated Methods

General Improvements Needed:

1. Network Services:

· Timeout handling (all checkers)
· DNS resolution failures
· Connection refused scenarios
· Rate limiting responses
· SSL/TLS certificate errors

2. File System Operations:

· Permission denied
· Disk full
· Read-only filesystem
· Broken symlinks
· UTF-8 filename encoding

3. Android-Specific:

· Termux API not installed
· Termux API out of date
· Missing Android permissions
· Battery optimization affecting scans
· Doze mode impacts

4. Command Execution:

· Subprocess timeout
· Command not found
· Output parsing failures
· Large output handling
· Unicode decode errors

5. Configuration:

· Missing config file
· Corrupted JSON
· Invalid values
· Default fallback
· Migration issues

---

🎯 Test Priorities Matrix

Priority Module Method Type Effort Impact
P0 sms.py SMSChecker.check C High Critical
P0 renderer.py render_network_metrics C High Critical
P0 network.py TelephonyModel.from_dict C Medium Critical
P1 renderer.py _format_signal_strength B Low High
P1 wifi.py WifiChecker.check B Medium High
P1 hotspot.py HotspotChecker.check B Medium High
P1 sensors.py SensorCollector.get_sensor_data B Medium High
P2 All Edge cases (timeouts/permissions) A High Medium
P3 All Integration tests A High Low

---

📈 Success Criteria

For C-Rated Methods:

· Achieve 95%+ coverage
· All failure paths tested
· Mock external dependencies properly
· Integration tests added

For B-Rated Methods:

· Achieve 95%+ coverage
· Test all edge cases
· Verify return value structure

For A-Rated Methods:

· Add missing edge case tests
· Improve assertion specificity
· Test error scenarios

Overall Targets:

· 98% total coverage
· 0 C-rated methods
· 0 B-rated methods
· All tests < 100ms each
· No flaky tests

---

🛡️ Type Safety Implementation Strategy (Mypy Strict)

Goal: Resolve 122+ Mypy errors identified in the latest scan, transitioning the project to full type strictness.

Strategy:

1.  Integrate with C/B-Rated Refactoring:
    · Fix all type errors within a file when refactoring its C-rated or B-rated methods.
    · Add return type annotations to all functions.
    · Fix missing generic type arguments (e.g., `dict[str, Any]`, `list[str]`).
    · Properly annotate all variables, especially in complex logic.

2.  Remaining Files (A-Rated):
    · Once core refactoring is done, systematically resolve type errors in A-rated files, focusing on:
      · Fixing `Any` returns.
      · Resolving `no-untyped-call` errors by annotating dependencies.
      · Fixing `assignment` and `arg-type` compatibility issues.

3.  Enforcement:
    · Add `make lint` to include `mypy --strict src/`
    · Update `.github/workflows/ci.yml` to fail on type check errors.

Week 1 - Critical Fixes:

1. SMSChecker.check - comprehensive tests [✓ DONE]
2. render_network_metrics - refactor + test [✓ DONE]
3. TelephonyModel.from_dict - test suite [✓ DONE]

Week 2 - B-Rated Methods:

1. Signal strength tests [✓ DONE]
2. WiFi checker tests [✓ DONE]
3. Hotspot tests [✓ DONE]
4. Sensor tests [✓ DONE]

Week 3 - Edge Cases:

1. Timeout handling [✓ DONE]
2. Permission denied scenarios
3. API availability fallbacks
4. Data validation

Week 4 - Integration:

1. End-to-end workflows
2. Performance benchmarks
3. Documentation updates
4. Code review

---

✅ Action Items

· Create test fixtures for SMS data (mock ContentResolver)
· Refactor render_network_metrics into 5 methods
· Add TelephonyModel test data factory
· Mock all network interfaces for WiFi/Hotspot tests
· Create sensor data fixtures
· Add timeout simulation decorators
· Implement permission denied mocks
· Create Android environment fixtures
· Add integration test suite
· Set up CI pipeline with coverage reporting

---

🎯 Final Checklist

· All C methods → A or B rating
· All B methods → A rating
· Total coverage > 98%
· All tests deterministic
· No external API calls in tests
· Fixtures reusable across test files
· Test documentation complete
· CI pipeline passes
