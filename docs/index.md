# md.python.measure

md.python.measure is a component that provides measure API.

## Architecture overview

[![Architecture overview][architecture-overview]][architecture-overview]

## Install

```sh
pip install md.python.measure --index-url https://source.md.land/python/
```

## Usage example
### Time measure

`md.python.measure.Time` component designed to measure operation time, for example:

=== "Single operation"

    ```python3
    import time
    import md.python.measure
    
    if __name__ == '__main__':
        with md.python.measure.Time() as measure:
            time.sleep(0.42)  # your operation, for example ...
    
        print(    
            f'Operation started at `{measure.start!s}`, '
            f'finished at `{measure.end!s}` '
            f'and took `{measure.time()}` seconds'
        )
    ```

    will print:
    
    ```
    Operation started at `0.070828782`, finished at `0.493188167` and took `0.42235938500000003` seconds
    ```

=== "Repeating operation"

    ```python3
    import random
    import time
    import md.python.measure
    
    if __name__ == '__main__':
        times = []
    
        measure = md.python.measure.Time()
        for _ in range(42):
            with measure:
                time.sleep(random.random() * 1.42)
            times.append(measure.time())
    
        print('Average: ', sum(times) / len(times))
    ```

    will print:
    
    ```
    Average:  0.6556656944047619
    ```

typically, it may be required for statistic purposes:

```python3
import psr.log
import md.python.measure

if __name__ == '__main__':
    logger: psr.log.LoggerInterface = ...
    
    with md.python.measure.Time() as measure:
        pass  # your operation
    
    logger.notice('Important blocking operation done successful', {'duration': measure.time()})
```

#### Set now function

By default, monotonic clock (`time.monotonic` function) is used to get current time,
if different driver is required `now` argument should be passed in constructor, 
for example:

```python3
import time
import md.python.measure

if __name__ == '__main__':
    with md.python.measure.Time(now=time.time) as measure:
        time.sleep(0.42)

    print(
        f'Operation started at `{measure.start!s}`, '
        f'finished at `{measure.end!s}` '
        f'and took `{measure.time()}` seconds'
    )
```

```
Operation started at `1675068910.211057`, finished at `1675068910.632562` and took `0.4215049743652344` seconds
```

#### Offline measure

`md.python.measure.Time` component could be used to measure duration with preset timings,
for example:

```python3
import md.python.measure

if __name__ == '__main__':
    measure = md.python.measure.Time(start=4.0, end=42.0)
    assert measure.time() == 38.0

    # ... and reused:
    with measure:
        import time
        time.sleep(0.42)
        measure.time()
```

[architecture-overview]: _static/architecture-overview.class-diagram.svg
