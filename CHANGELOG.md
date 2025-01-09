# CHANGELOG


## v0.3.0-rc.1 (2025-01-09)

### Bug Fixes

- Directory clean to use constants (#54) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`948e214`](https://github.com/scope3data/scope3ai-py/commit/948e21431b729e4ba33754c8844ab7dffcc6763b))

- Hugging face async coverage (#44) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`4b41096`](https://github.com/scope3data/scope3ai-py/commit/4b41096d7c022b5657f435bd9ca9fb392e103b0a))

- Use local model cost for tests (#49) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`5a572e8`](https://github.com/scope3data/scope3ai-py/commit/5a572e8fdb8c2d85d5120cfdf252774afbfe1d2c))

### Documentation

- Update README for openai support (#51) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`e2cef38`](https://github.com/scope3data/scope3ai-py/commit/e2cef381dcfbc7d4ffe82ee91629dd8f781b74b7))

### Features

- Response interceptor aiohttp / requests (#48) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`6a3806b`](https://github.com/scope3data/scope3ai-py/commit/6a3806b9d19736c09070e6f8687c973a319bb4ea))

- **huggingface**: Add support for image-to-image/ text-to-speech (#56)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`4bcd2dd`](https://github.com/scope3data/scope3ai-py/commit/4bcd2dd7dfca6dc7d0290a82111c83e75de8c511))

- **huggingface**: Support for async translation (#52)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`c7946de`](https://github.com/scope3data/scope3ai-py/commit/c7946de6196425f5bd9ce0aa3d3379a860925bf2))

- **mistralai**: Support for mistralai v1 chat (#46)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`e9ebd28`](https://github.com/scope3data/scope3ai-py/commit/e9ebd28ceb79b9e489727d841e3ed86d31ea14b0))

- **openai**: Add support for speech to text (#50)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`05c1947`](https://github.com/scope3data/scope3ai-py/commit/05c19478b4cbd491f5dc478f5d12dd38b5b94783))

- **openai**: Add support for speech translation (#57)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`5ada606`](https://github.com/scope3data/scope3ai-py/commit/5ada606b7dcced3c58b9023e554d693db7a50bae))

- **openai**: Support for image generation (#55)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`7f6277b`](https://github.com/scope3data/scope3ai-py/commit/7f6277b7e33070344911c9ea51eac31de0edc18c))

- **openai**: Support for text-to-speech (#45) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`3f7a316`](https://github.com/scope3data/scope3ai-py/commit/3f7a316e4d8e873d053664cdb642bda307728694))


## v0.2.1 (2024-12-31)

### Bug Fixes

- **api**: Tests and fix unused code on api (#38)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`19ba2d4`](https://github.com/scope3data/scope3ai-py/commit/19ba2d4bef2249663f1856b1e127222f57b9808e))

- **openai**: Fix async report and add unit tests (#39)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`1497a9e`](https://github.com/scope3data/scope3ai-py/commit/1497a9e6f0f2e72f8b5aef8855e44dba1f348eb1))

- **tracer**: Fix tracer.asubmit_impact and add more tests (#37)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`1028ea2`](https://github.com/scope3data/scope3ai-py/commit/1028ea2aa799be6ed9fa40113ab22be7117536e7))

- **tracer**: Fixes asubmit_impact that was not working + unittest (#41)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`640317c`](https://github.com/scope3data/scope3ai-py/commit/640317c96c792f13a8fa11a983e0d7780f48d6ef))

- **worker**: Add more unit tests and fix some behavior of the worker (#36)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`a29101f`](https://github.com/scope3data/scope3ai-py/commit/a29101f5223f86a8c3bba12055cd895ab3a9cdad))

### Chores

- **release**: 0.2.1 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`11d0204`](https://github.com/scope3data/scope3ai-py/commit/11d02043e26dc26df3ce62f0281a755c32f200df))

- **tracer**: Remove dead code in tracer (#40) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`f56f06c`](https://github.com/scope3data/scope3ai-py/commit/f56f06c13723de167611a8a83c38959b9d1e9ff7))

### Documentation

- **readme**: Include python version and pytests status (#42)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`559188a`](https://github.com/scope3data/scope3ai-py/commit/559188ab27e1328544a080faffb83a715049afa6))

- **readme**: Update README.md (#43) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`e765157`](https://github.com/scope3data/scope3ai-py/commit/e76515763830e8b2ac535f58046ac67f4bb77aca))


## v0.2.0 (2024-12-31)

### Chores

- **release**: 0.2.0 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`99dfa7b`](https://github.com/scope3data/scope3ai-py/commit/99dfa7b8753d443fc3b8abd489f5fc6543c929f4))

### Continuous Integration

- **coveralls**: Add support for coveralls (#35)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`4cddb64`](https://github.com/scope3data/scope3ai-py/commit/4cddb6439eb45759482a0eb661b0efda070a9f92))

### Documentation

- **openai**: Add OpenAI chat examples using chat interface (#33)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`9fcc2e5`](https://github.com/scope3data/scope3ai-py/commit/9fcc2e530468b9595d17152c430911e05d9072fb))

### Features

- **anthropic**: Support for messages.create(stream=True) + add chat examples (#34)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`4598bdf`](https://github.com/scope3data/scope3ai-py/commit/4598bdf7ebd5a73ca597a95fc811174f66d5b7d1))


## v0.1.0 (2024-12-27)

### Build System

- Add classifiers to the project (#31) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`d09bff9`](https://github.com/scope3data/scope3ai-py/commit/d09bff979400f4c32a814cd04227208aaf7bec5f))

### Chores

- **release**: 0.1.0 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`b4f2dbc`](https://github.com/scope3data/scope3ai-py/commit/b4f2dbc8b91b7895788582f07f2a278dc9532616))


## v0.1.1-alpha.3 (2024-12-27)

### Chores

- **release**: 0.1.1-alpha.3 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`7ab542b`](https://github.com/scope3data/scope3ai-py/commit/7ab542b948a025e1395fac9c5ffc1f9048a9696e))

### Documentation

- Update readme with badge and compatibility matrix (#27)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`c4ad6cb`](https://github.com/scope3data/scope3ai-py/commit/c4ad6cb6fa3962fba1fd54ea0d97eca10eb47f05))

### Features

- **cohere**: Add support for Cohere client V1 (#29)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`60c6295`](https://github.com/scope3data/scope3ai-py/commit/60c62957198fddfa5f707cc6a213c3e1cd7926f3))

- **cohere**: Add support for v2 client + examples (#30)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`2f2850f`](https://github.com/scope3data/scope3ai-py/commit/2f2850f9770333bc69080f614d8cf8615a0c42ed))

- **litellm**: Litellm integration (#28) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`c1f56b9`](https://github.com/scope3data/scope3ai-py/commit/c1f56b9c1fb9e245ed637c41900e6b0749c975e1))


## v0.1.1-alpha.2 (2024-12-26)

### Chores

- **release**: 0.1.1-alpha.2 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`02c461f`](https://github.com/scope3data/scope3ai-py/commit/02c461f14c9ae2540c2b25eeb02554a749459f0f))

### Features

- **tracer**: Add impact and synchronisation in tracer (#26)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`f48b63c`](https://github.com/scope3data/scope3ai-py/commit/f48b63ce8137cf2d8855e9c76539d956221316d3))


## v0.1.1-alpha.1 (2024-12-24)

### Build System

- Rename the project from scope3ai-py to scope3ai for easier installation (#24)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`e5f9356`](https://github.com/scope3data/scope3ai-py/commit/e5f93569ce098201f4d155665b3ffc4689bf8fec))

### Chores

- **release**: 0.1.1-alpha.1 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`e5754da`](https://github.com/scope3data/scope3ai-py/commit/e5754dae5a9d8a9b8d6984162ecaa9c903170148))

### Testing

- Move the mp3 to appropriate location in tests/data (#25)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`1a080b0`](https://github.com/scope3data/scope3ai-py/commit/1a080b08062a9d5ecd846f97a82e0d4a6dd42bb2))


## v0.1.0-alpha.2 (2024-12-24)

### Bug Fixes

- Fix the workflow (#23) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`760e177`](https://github.com/scope3data/scope3ai-py/commit/760e1776ab0066381244b4f4d13962e8ce378035))

- Prevent uv.lock to be out of sync after release (#22)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`2db0d78`](https://github.com/scope3data/scope3ai-py/commit/2db0d78b889eaea688c224d4edbd4fd21c198342))

### Chores

- **release**: 0.1.0-alpha.2 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`6c7eaa9`](https://github.com/scope3data/scope3ai-py/commit/6c7eaa9d5c009ed6614dcd6877f21c517c540404))

### Continuous Integration

- Update package name (#21) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`2733f5f`](https://github.com/scope3data/scope3ai-py/commit/2733f5fc9f6837d0f9c3b981787f657f5914d148))


## v0.1.0-alpha.1 (2024-12-24)

### Bug Fixes

- Pydantic deprecation max_items to max_length (#4)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`bf5f7b3`](https://github.com/scope3data/scope3ai-py/commit/bf5f7b353fac1907dbe8754d5a1c7779390a32a4))

### Chores

- **release**: 0.1.0-alpha.1 ([](https://github.com/scope3data/scope3ai-py/pull),
  [`0d30557`](https://github.com/scope3data/scope3ai-py/commit/0d30557437d483fb7d1ebe7a6e2504cdadf3f3fd))

- **release**: Allow release workflow to commit on main (#15)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`bdace37`](https://github.com/scope3data/scope3ai-py/commit/bdace37698b6143d84072d30ef831bd567f97bd4))

### Continuous Integration

- Add conventional commit workflow ([](https://github.com/scope3data/scope3ai-py/pull),
  [`2e7339f`](https://github.com/scope3data/scope3ai-py/commit/2e7339fdeaf1fb5284e41f9a77ddfa7472f3cdb8))

- Add pre-commit workflow ([](https://github.com/scope3data/scope3ai-py/pull),
  [`928fe65`](https://github.com/scope3data/scope3ai-py/commit/928fe656ae326022472378c96ee4d37908839e0f))

- Add release workflow (#14) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`8686f76`](https://github.com/scope3data/scope3ai-py/commit/8686f7630c6deda02d66acb246496fd4468fda6a))

- Add ssh information for python-semantic-release (#16)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`d2466ba`](https://github.com/scope3data/scope3ai-py/commit/d2466baba846602a8eb54843b5795e208aade9e7))

- Add uv build in release (#20) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`cbb8f74`](https://github.com/scope3data/scope3ai-py/commit/cbb8f742ba383e589bff6c8a06dcd8c03af0e0ed))

- Ensure PR title are matching conventional commit spec (#11)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`d922b6e`](https://github.com/scope3data/scope3ai-py/commit/d922b6e26eb07c87f412114c7777c7f5a9c58e9d))

- Introduce python-semantic-release (#13) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`7e345a5`](https://github.com/scope3data/scope3ai-py/commit/7e345a5f3c4aecdb74540cd06a50a0829e76ecd4))

- Try fixing cocogitto integration ([](https://github.com/scope3data/scope3ai-py/pull),
  [`4438ad7`](https://github.com/scope3data/scope3ai-py/commit/4438ad7c4bc17e8f64d12bf0aec94dc032b73a1f))

- Try fixing git push (#19) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`30071b8`](https://github.com/scope3data/scope3ai-py/commit/30071b806c3c32cfd6161a562c7bb4c649582b92))

- Try manual push (#18) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`b80c2f7`](https://github.com/scope3data/scope3ai-py/commit/b80c2f70f65d0ac4100e21f8909dabba80c881de))

- Try using PAT (#17) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`80026e5`](https://github.com/scope3data/scope3ai-py/commit/80026e58e79232d99169a23473608fc89a298635))

### Features

- Add anthropic chat support (#9) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`12c4a8a`](https://github.com/scope3data/scope3ai-py/commit/12c4a8a23182170a0d403885d95fbe871a987dd4))

- First http sync/async client ([](https://github.com/scope3data/scope3ai-py/pull),
  [`2c0d4ec`](https://github.com/scope3data/scope3ai-py/commit/2c0d4ec66a081c229e1bf5234cba5a36bfc0721f))

- Hugging face chat and image generation first iteration (#7)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`c230c94`](https://github.com/scope3data/scope3ai-py/commit/c230c9460a8534930c38ab3adb80f756e78146a4))

- Hugging face headers (#12) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`c37e831`](https://github.com/scope3data/scope3ai-py/commit/c37e83187e86fd0488079f7fdd3a1f5c2efcaa64))

- Initial incomplete proposal for scope3ai library
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`c4a3f28`](https://github.com/scope3data/scope3ai-py/commit/c4a3f28c0bb40dcf0803004a27ac4e6d444fa4ab))

- Initial pytest implementation for openai (#5) ([](https://github.com/scope3data/scope3ai-py/pull),
  [`7490ab7`](https://github.com/scope3data/scope3ai-py/commit/7490ab7f027e61bd53348a0adf5403615f999c9e))

- Initial unit test implementation using PyVcr (#3)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`2a3df02`](https://github.com/scope3data/scope3ai-py/commit/2a3df027c7f58b61e38556cce0b560dc53360851))

- Use pydantic codegen to generate types from OpenAPI Scope3AI (#6)
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`24e8652`](https://github.com/scope3data/scope3ai-py/commit/24e86527647cb8219ff8f50a9cbf5a96355bfb3e))

### Refactoring

- Rework the initial tracer and add parenting flow
  ([](https://github.com/scope3data/scope3ai-py/pull),
  [`559c822`](https://github.com/scope3data/scope3ai-py/commit/559c822c107b9fcb57b506ebdb591f3dbe4724d7))


## v0.0.1 (2024-12-09)

### Features

- Initial commit ([](https://github.com/scope3data/scope3ai-py/pull),
  [`cccf93a`](https://github.com/scope3data/scope3ai-py/commit/cccf93afc07aa4d3b860334afd1668da12ca8633))

