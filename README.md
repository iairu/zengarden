# Zen Garden (Tabu search evolution)

## Map generator and samples

Adujst and use `python __map_generator__.py` to generate samples. Pre-generated `map_samples` are already bundled in this repo, so there isn't a need to run this. I've also included a `hint.png` file to quickly glance at the generated samples and easily notice the placement of pebbles.

Generator is not ideal - it **doesn't** try to generate fields that are guaranteed to be eventually solvable. The  `generate()` function can be adjusted to lower/increase the amount of pebbles, however that still won't guarantee solvability.

## Main

1. A sample from the `map_samples` folder will get loaded and printed.
2. todo: Random gene-pool will get created.