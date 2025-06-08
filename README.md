### Configuration

```
glidepoint: glidepoint@2a {
    compatible = "cirque,pinnacle";
    ...

    // Enable and configure pointer acceleration
    polynomial-acceleration;
    acceleration-factor=<150>;
    acceleration-threshold=<600>;
};
```
Factor & threshold is divided by 100 to get a proper float value (zephyr only supports int as property type)

### Strategies comparison

![image](docs/comparison.png)
