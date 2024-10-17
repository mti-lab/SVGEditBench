# SVGEditBench
This repository contains the dataset used for the "SVGEditBench: A Benchmark Dataset for Quantitative Assessment of LLM's SVG Editing Capabilities" paper ([CVF](https://openaccess.thecvf.com/content/CVPR2024W/GDUG/papers/Nishina_SVGEditBench_A_Benchmark_Dataset_for_Quantitative_Assessment_of_LLMs_SVG_CVPRW_2024_paper.pdf), [arXiv](http://arxiv.org/abs/2404.13710)). The paper was accepted to [Workshop on Graphic Design Understanding and Generation (GDUG)](https://sites.google.com/view/gdug-workshop), held at the [CVPR2024](https://cvpr.thecvf.com/Conferences/2024) conference.

## Structure of the Dataset
The benchmark consists of six SVG editing tasks, each with its own folder. Each folder has two subfolders: `answer` and `query`. The `query` folder contains the prompt for the LLM with the SVG code before editing. The `answer` folder is where the answer images are.

We selected 100 images from the [twemoji](https://github.com/twitter/twemoji) dataset (by Twitter, Inc and other contributors, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) and made the input prompt and the answer images. The images were modified to create those answer images. Refer to the paper for more details on how we created the dataset.

## Usage
To use the dataset to test your own LLM, clone the repository and input the prompts in the `query` folder to the LLM.

If you want to change the number of cases, try out a new task, or use a different dataset to generate the cases, you can build your own dataset with the `CaseGenerator.py` code. Follow these steps to do so:

1. Copy the `CaseGenerator.py` file.
2. Clone the [twemoji](https://github.com/twitter/twemoji) dataset in the same folder as the downloaded `CaseGenerator.py` file.
> [!NOTE]
> If you plan to use a different SVG dataset, make sure to update the path to the SVG files and the name for each image in the `CaseGenerator.py` file.
3. Run the code.
> [!Tip]
> Use the latest version of Python to minimize the possibility of images not being included in the dataset due to the absence of the emoji names in the `unicodedata` library.
4. The dataset will be built in the same structure as this repository.

## License
- Code and prompts licensed under the [MIT License](https://opensource.org/license/mit)
- Images licensed under the [CC-BY 4.0 License](https://creativecommons.org/licenses/by/4.0/)
