from web3 import AsyncWeb3
import httpx
import asyncio


async def mint(to, rpc, private_key, maxFeePerGas, maxPriorityFeePerGas, data):
    RPC = rpc
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    http = httpx.AsyncClient()
    chain_id = await web3.eth.chain_id
    to = web3.to_checksum_address(to)
    nonce = await web3.eth.get_transaction_count(account.address)
    maxFeePerGas = int(maxFeePerGas)
    maxPriorityFeePerGas = int(maxPriorityFeePerGas)
    maxFeePerGas = web3.to_wei(maxFeePerGas, 'gwei')
    maxPriorityFeePerGas = web3.to_wei(maxPriorityFeePerGas, 'gwei')
    for x in range(0, 100):
        request_list = []
        for i in range(0, 100):
            tx = {
                'from': account.address,
                'to': to,
                'nonce': nonce,
                'gas': 25024,
                'maxFeePerGas': maxFeePerGas,
                'maxPriorityFeePerGas': maxPriorityFeePerGas,
                'chainId': chain_id,
                'data': data
            }
            signed = account.sign_transaction(tx)
            nonce += 1
            request_list.append({"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": [signed.rawTransaction.hex()], "id": i + 1})
        res = await http.post(RPC, json=request_list)
        await asyncio.sleep(1)
        print(res.json())

if __name__ == '__main__':
    print('hdd.cm, 推特低至2毛')
    _to = input('输入地址(打到那个号)：').strip()
    _private_key = input('输入私钥(有gas的小号)：').strip()
    _rpc = input('输入RPC：').strip()
    _maxFeePerGas = input('输入maxFeePerGas：').strip()
    _maxPriorityFeePerGas = input('输入maxPriorityFeePerGas：').strip()
    _data = input('输入data：').strip()
    asyncio.run(mint(_to, _rpc, _private_key, _maxFeePerGas, _maxPriorityFeePerGas, _data))
