# How to set up

1. Build docker image
   ```shell
   make build_test_env
   ```

2. Run docker container
   ```shell
   make start
   ```
3. Run tests
   
   1. all tests
      ```shell
      make test spec
      ```
   2. run all tests in a file
      ```shell
      make test spec=tests/test_sqls.py
      ```
   3. run specific test function 
      ```shell
      make test spec=tests/test_sqls.py::test_customers
      ```
   4. run specific spec
      ```shell
      make test spec=tests/test_sqls.py::test_spec name=run_products
      ```
4. Stop docker container
    ```shell
   make stop
    ```