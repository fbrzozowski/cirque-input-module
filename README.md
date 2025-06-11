> [!CAUTION]
> This is work in progress feature!
 
### Modes Comparison
Personally I like the feel of hybrid - more responsive/aggressive, ideal for the 40mm small form factor trackpad. You should play around with the values. Below is a good starting point and visualised acceleration vales. 

| Mode    | Threshold (T) | Factor (F) | Exponent (E) |
| ------- |---------------|------------|--------------|
| HYBRID  | 128           | 500        | 155          |
| SIGMOID | 850           | 165        | n/a          |

> [!NOTE]
> F, T & E variables are divided by 100 (POINTER_ACCELERATION_SCALE) to convert them into appropriate float values. By default, Zephyr only supports integers for property types.

> [!CAUTION]
> `Threshold` for hybrid mode is not divided!!! Think of this value as acceleration limit taper starting point (exact limit is `threshold*factor`). Look at the second graph.

![image](docs/comparison.png)
#### Hybrid with lower acceleration limit
![acceleration limit](docs/hybrid-limits.png)

### Sample Configuration

```
glidepoint: glidepoint@2a {
    compatible = "cirque,pinnacle";
    ...

    // Enable and configure pointer acceleration (choose one!)
    acceleration-mode="NONE|HYBRID|SIGMOID";
    acceleration-threshold=<128>; //Curve limit for hybrid acceleration
    acceleration-factor=<500>;
    acceleration-exponent=<155>;
};
```

### TODO
- [x] Replace `tanhf` w/ lookup table
- [x] Benchmark 'input lag' with each acceleration functions
  - [hybrid acc. runtime vs lookup table](docs/benchmarks/benchmarks.md)
- [ ] Config for explicit X/Y acceleration curves (X axis should be more responsive) - could be accomplished w/ `&zip_x_scaler` 
- [x] Enum for configuring acceleration strategy (preventing enabled 2 accelerations strategies at the same time)
- [ ] Add pointer smoothing (data report interval???)

