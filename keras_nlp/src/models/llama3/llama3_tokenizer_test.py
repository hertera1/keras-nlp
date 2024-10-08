# Copyright 2024 The KerasNLP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from keras_nlp.src.models.llama3.llama3_tokenizer import Llama3Tokenizer
from keras_nlp.src.tests.test_case import TestCase


class Llama3TokenizerTest(TestCase):
    def setUp(self):
        self.vocab = ["!", "air", "Ġair", "plane", "Ġat", "port"]
        self.vocab += ["<|end_of_text|>", "<|begin_of_text|>"]
        self.vocab = dict([(token, i) for i, token in enumerate(self.vocab)])
        self.merges = ["Ġ a", "Ġ t", "Ġ i", "Ġ b", "a i", "p l", "n e"]
        self.merges += ["Ġa t", "p o", "r t", "Ġt h", "ai r", "pl a", "po rt"]
        self.merges += ["Ġai r", "Ġa i", "pla ne"]
        self.init_kwargs = {"vocabulary": self.vocab, "merges": self.merges}
        self.input_data = [
            "<|begin_of_text|>airplane at airport<|end_of_text|>",
            " airplane airport",
        ]

    def test_tokenizer_basics(self):
        self.run_preprocessing_layer_test(
            cls=Llama3Tokenizer,
            init_kwargs=self.init_kwargs,
            input_data=self.input_data,
            expected_output=[[7, 1, 3, 4, 2, 5, 6], [2, 3, 2, 5]],
        )

    def test_errors_missing_special_tokens(self):
        with self.assertRaises(ValueError):
            Llama3Tokenizer(vocabulary={"foo": 0, "bar": 1}, merges=["fo o"])

    @pytest.mark.large
    def test_smallest_preset(self):
        self.run_preset_test(
            cls=Llama3Tokenizer,
            preset="llama3_8b_en",
            input_data=["The quick brown fox."],
            expected_output=[[791, 4062, 14198, 39935, 13]],
        )

    @pytest.mark.extra_large
    def test_all_presets(self):
        for preset in Llama3Tokenizer.presets:
            self.run_preset_test(
                cls=Llama3Tokenizer,
                preset=preset,
                input_data=self.input_data,
            )
