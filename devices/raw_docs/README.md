# Example Device Documentation

This folder contains raw device documentation that will be automatically parsed by the AI-IoT Hub.

## Supported Formats

### PDFs
Drop any PDF manual, API documentation, or specification document:
- `honeywell_t6_pro_manual.pdf`
- `nest_thermostat_api_guide.pdf`
- `modbus_sensor_datasheet.pdf`

### URLs (as .txt files)
Create a .txt file containing a single URL to online documentation:
- `nest_api_docs.txt` → contains `https://developers.nest.com/reference`
- `zigbee_spec_link.txt` → contains `https://zigbeealliance.org/wp-content/uploads/2019/11/docs-05-3474-21-0csg-zigbee-specification.pdf`

### Word Documents
Drop .docx files with device specifications:
- `custom_sensor_protocol.docx`
- `device_integration_guide.docx`

## Auto-Processing

When you add files here:

1. **Spec Generation**: The AI will automatically parse the documentation and generate structured JSON specs in `devices/generated_specs/`

2. **Code Generation**: When you request device communication, the AI will generate Python communication code in `tools/generated/`

3. **Caching**: Generated specs and tools are cached for performance

## Example Structure

```
thermostats/
├── honeywell_t6_manual.pdf
├── nest_api_docs.txt
└── ecobee_integration_guide.docx

sensors/
├── zigbee_sensor_spec.pdf
├── modbus_temp_sensor.txt
└── custom_iot_device.docx
```

The AI will automatically detect device types based on folder structure and content analysis.