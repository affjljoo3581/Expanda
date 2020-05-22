expanda.ext.namuwiki
====================

Introduction
------------
**나무위키**\([#]_)는 대표적인 한국어 기반 위키입니다. 다른 나라와는 달리, 한국어 위키의
경우 위키피디아([#]_)보다 나무위키가 더 큰 규모를 가지고 있습니다. 문서 주제가 다소 편향된
경향이 있지만, 기본적으로 위키이기 때문에 다양한 분야의 문서를 보유하고 있습니다. 나무위키는
문서에 기여하는 사용자가 매우 많습니다. 그로 인해 나무위키가 보유하고 있는 문서 수와 그
규모는 압도적입니다.

나무위키 또한 다른 위키들처럼 **주기적으로 백업된 덤프 파일**\을 제공합니다. 이에 관한
내용은 `여기`_\를 참고하시기 바랍니다. 나무위키가 제공하는 덤프 파일 중에서, Expanda는
``json`` 형식을 지원합니다. Corpus로 제작하고자 하는 나무위키 ``json`` 덤프 파일을
다운받은 후, 설정 파일에서 덤프 파일을 명시하여 빌드하면 됩니다.

해당 extension은 나무위키의 문법인 *나무마크*\를 완벽하게 지원하지는 않습니다. 기본적인
코드 정리 및 문장 정제 과정을 거쳐 corpus로 쓸 만한 형태로 파싱합니다. 따라서 몇몇
문장들은 어색하거나 알 수 없는 코드들이 남아있을 수 있습니다. 속도와 복잡성 등을 고려할 때,
저희는 해당 절충안이 성능 저하를 최소화하는 적절한 수준이라고 판단합니다. 나무위키의
데이터는 매우 크기 때문에, 약간의 text noise는 문제가 되지 않습니다.

.. caution::
    나무위키의 문서를 병렬적으로 파싱하기 위해, `temporary` 폴더 내에 분할 파일들이
    생성됩니다. 해당 extension을 실행하는 도중에 임시 파일들이 삭제되지 않도록 조심해
    주시기 바랍니다.

Expanda는 몇 가지의 실험을 바탕으로, 빠른 속도로 나무위키 corpus를 생성합니다.
대략적으로, 12.5GB의 나무위키 json 파일을 사용하여 해당 extension을 실행하는 데 6분
정도가 소요됩니다.

Details
-------
.. code:: console

    $ expanda show expanda.ext.namuwiki
    Extension [expanda.ext.namuwiki]
    Name             : namuwiki extractor
    Version          : 1.0
    Description      : extract namuwiki json file.
    Author           : expanda
    Parameters
        num-cores    : int    (default: 1)
        min-length   : int    (default: 50)

Configuration Example
---------------------
.. code:: ini

    # ...

    [expanda.ext.wikipedia]
    num-cores           = 8
    min-length          = 100

    # ...

References
----------
.. [#] https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4
.. [#] https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC
.. _`여기`: https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EB%8D%A4%ED%94%84
