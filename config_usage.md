完整的config文件包含`pallet_*` ，`runtime_constant` 和`chain_spec_*`三部分。

**如果不需要某个pallet，则直接将该pallet的整个配置段移除。**

如果不确定某部分参数如何填写，则尽量保持与该config配置一致。

### 1. `pallet_*`

每个pallet里面主要包含`parameter` 、`chain_spec` 和 `rpc_mod`。

`parameter`用来配置runtime里面的参数。

`chain_spec` 用来配置node里面的chain_spec.rs里面的genesisConfig参数。

`rpc_mod`是一个bool变量，用于控制node里面的RPC模块是否启用当前pallet的RPC功能，如果pallet没有RPC功能，则修改不会生效。

### 2. `runtime_constant`

这里包含了runtime可能需要用户修改的宏。

### 3. `chain_spec_*`

包含了genesisConfig的参数，这里面的参数都必须填写。
如果使用DOT作为gas费，tokenSymbol则填写DOT，如果不填写，则默认使用DOT作为tokenSymbol。

```json
{
  "pallet_frame_system": {
    "index": 0,
    "optional": false,
    "parameter": {
      "RuntimeVersion": {
        "spec_name": "magnet-parachain",
        "impl_name": "magnet-parachain",
        "authoring_version": 1,
        "spec_version": 1,
        "impl_version": 0,
        "apis": "RUNTIME_API_VERSIONS",
        "transaction_version": 1,
        "state_version": 1
      },
      "RuntimeBlockLength": "5 * 1024 * 1024", //这个地方也可以是一个整数
      "SS58Prefix": 42
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_timestamp": {
    "index": 1,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_authorship": {
    "index": 2,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_balances": {
    "index": 3,
    "optional": false,
    "parameter": {
      "MaxLocks": 50,
      "ExistentialDeposit": "EXISTENTIAL_DEPOSIT", //这个地方也可以修改成整数，或者一个表达式:`n * EXISTENTIAL_DEPOSIT`，因为 EXISTENTIAL_DEPOSIT在代码里是一个宏定义
      "MaxReserves": 50,
      "MaxFreezes": 1
    },
    "chain_spec": {
      "endowed_accounts_supply": "1u128 << 81"  //这里也可以是一个整数，表示预制账户的total supply, 这里通过右移运算计算出了一个比较大的数字
    },
    "rpc_mod": false
  },
  "pallet_transaction_payment": {
    "index": 4,
    "optional": false,
    "parameter": {
      "TransactionByteFee": 10,
      "OperationalFeeMultiplier": 5
    },
    "chain_spec": {},
    "rpc_mod": true
  },
  "pallet_sudo": {
    "index": 5,
    "optional": false,
    "parameter": {},
    "chain_spec": {
      "keyFromAddress": "5HQDD5z4qMwPtkCcxwRntmbjGJ5oU7DgJDTmJGChCXZKcrm1"
    },
    "rpc_mod": false
  },
  "cumulus_pallet_parachain_system": {
    "index": 6,
    "optional": false,
    "parameter": {
      //这下面的三个参数都可以不用修改，不传人会默认适配
      "ReservedXcmpWeight": "MAXIMUM_BLOCK_WEIGHT.saturating_div(4)",
      "ReservedDmpWeight": "MAXIMUM_BLOCK_WEIGHT.saturating_div(4)",
      "RelayOrigin": "AggregateMessageOrigin::Parent"
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "parachain_info": {
    "index": 7,
    "optional": false,
    "parameter": {},
    "chain_spec": {
      "parachainId": 2000
    },
    "rpc_mod": false
  },
  "pallet_message_queue": {
    "index": 8,
    "optional": false,
    "parameter": {
      "MessageQueueServiceWeight": 35,
      "HeapSize": "64 * 1024", //这里可以是整数或者表达式
      "MaxStale": 8
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "cumulus_pallet_aura_ext": {
    "index": 9,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "cumulus_pallet_xcm": {
    "index": 10,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "cumulus_pallet_xcmp_queue": {
    "index": 11,
    "optional": false,
    "parameter": {
      "MaxInboundSuspended": "1_000" //这里可以是整数
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_session": {
    "index": 12,
    "optional": false,
    "parameter": {
      "Period": "6 * HOURS", //这里可以是整数，或者`n * HOURS`表达式
      "Offset": 0
    },
    "chain_spec": {
      "keys": []
    },
    "rpc_mod": false
  },
  "pallet_aura": {
    "index": 13,
    "optional": false,
    "parameter": {
      "MaxAuthorities": "100_000", //这里可以是整数
      "AllowMultipleBlocksPerSlot": "false" //这里需要传字符串的 true 或者false, 不然代码转换换变成python的`True`或者`False`
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_collator_selection": {
    "index": 14,
    "optional": false,
    "parameter": {
      "PotId": "PotStake",
      "SessionLength": "6 * HOURS", //这里可以是整数，或者`n * HOURS`表达式
      "StakingAdminBodyId": "BodyId::Defense",
      "MaxCandidates": 100,
      "MinEligibleCollators": 4,
      "MaxInvulnerables": 20,
      "Period": "6 * HOURS" //这里可以是整数，或者`n * HOURS`表达式
    },
    "chain_spec": {
      "invulnerables": [],
      "candidacyBond": "EXISTENTIAL_DEPOSIT * 16" //这里可以是整数，或者`n * EXISTENTIAL_DEPOSIT`表达式
    },
    "rpc_mod": false
  },
  "pallet_bulk": {
    "index": 15,
    "optional": false,
    "parameter": {
      "MaxUrlLength": 300
    },
    "chain_spec": {
      "rpcUrl": "ws://127.0.0.1:8855",
      "genesisHash": "0x4ea18c8f295ba903acbbed39c70ea0569cf1705fa954a537ffa3b8b7125eaf58"
    },
    "rpc_mod": false
  },
  "pallet_on_demand": {
    "index": 16,
    "optional": false,
    "parameter": {},
    "chain_spec": {
      "slotWidth": 3,
      "priceLimit": 200000000,
      "gasThreshold": 10
    },
    "rpc_mod": false
  },
  "pallet_collective": {
    "index": 17,
    "optional": false,
    "parameter": {
      "CouncilMotionDuration": "7 * DAYS", //这里可以是整数，或者`n * DAYS`表达式
      "CouncilMaxProposals": 10,
      "CouncilMaxMembers": 25,
      "MaxCollectivesProposalWeight": 50
    },
    "chain_spec": {
      "members": []
    },
    "rpc_mod": false
  },
  "pallet_evm_chain_id": {
    "index": 18,
    "optional": false,
    "parameter": {},
    "chain_spec": {
      "chainId": 2000
    },
    "rpc_mod": false
  },
  "pallet_evm": {
    "index": 19,
    "optional": false,
    "parameter": {
      "SuicideQuickClearLimit": 0,
      "BlockGasLimit": "75_000_000", //这里可以是整数
      "MaxPovSize": "5 * 1024 * 1024" //这里可以是整数
    },
    "chain_spec": {
      "accounts": [
        {
          "address": "d43593c715fdd31c61141abd04a99fd6822c8558", //这里是去掉`0x`的evm地址格式
          "balance": "0xffffffffffffffffffffffffffffffff", //这里是16进制数字
          "code": "0x0", //这里可以添加evm账户的预编译code
          "nonce": "0x0",
          "storage": {}
        },
        {
          "address": "6be02d1d3665660d22ff9624b7be0551ee1ac91b",
          "balance": "0xffffffffffffffffffffffffffffffff",
          "code": "0x0",
          "nonce": "0x0",
          "storage": {}
        },
        {
          "address": "1000000000000000000000000000000000000001",
          "balance": "1_000_000_000_000_000_000_000_000u128",
          "code": "0x00",
          "nonce": "0x1",
          "storage": {}
        }
      ]
    },
    "rpc_mod": false
  },
  "pallet_ethereum": {
    "index": 20,
    "optional": false,
    "parameter": {
      "PostBlockAndTxnHashes": "PostLogContent::BlockAndTxnHashes",
      "ExtraDataLength": 30
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_dynamic_fee": {
    "index": 21,
    "optional": false,
    "parameter": {
      "BoundDivision": 1024
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_base_fee": {
    "index": 22,
    "optional": false,
    "parameter": {
      "DefaultBaseFeePerGas": "1_000_000_000", //这里可以是整数
      "DefaultElasticity": "125_000",//这里可以是整数
      "Ideal": "500_000",//这里可以是整数
      "Upper": "1_000_000"//这里可以是整数
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_hotfix_sufficients": {
    "index": 23,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_assets": {
    "index": 24,
    "optional": false,
    "parameter": {
      "AssetDeposit": "10 * UNIT", //这里可以是整数
      "AssetAccountDeposit": "deposit(1, 16)",
      "ApprovalDeposit": "EXISTENTIAL_DEPOSIT",
      "AssetsStringLimit": 50,
      "MetadataDepositBase": "deposit(1, 68)",
      "MetadataDepositPerByte": "deposit(0, 1)",
      "ExecutiveBody": "BodyId::Executive",
      "RemoveItemsLimit": 1000
    },
    "chain_spec": {
      "assets": [
        {
          "AssetsId": 1,
          "OwnerFromAddress": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
          "IsSufficient": "true",
          "MinBalance": "1_000_000_0000_0000_0000u128"
        },
        {
          "AssetsId": 2,
          "OwnerFromAddress": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
          "IsSufficient": "true",
          "MinBalance": "2_000_000_0000_0000_0000u128"
        }
      ],
      "metadata": [
        {
          //这里如果给账户地址预添加资产，下面的字段都需要添加
          "AssetsId": 1,
          "Name": "asset-1",
          "Symbol": "ALT1",
          "Decimals": 18
        },
        {
          "AssetsId": 2,
          "Name": "asset-2",
          "Symbol": "ALT2",
          "Decimals": 18
        }
      ],
      "accounts": [
        {
          "AssetsId": 1,
          "AccountIdFromAddress": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
          "Balance": "500_000_000_0000_0000_0000u128"
        },
        {
          "AssetsId": 2,
          "AccountIdFromAddress": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
          "Balance": "500_000_000_0000_0000_0000u128"
        }
      ]
    },
    "rpc_mod": false
  },
  "pallet_assets_bridge": {
    "index": 25,
    "optional": false,
    "parameter": {
      "EvmCaller": "[17u8;20]",
      "ClaimBond": "10 * EXISTENTIAL_DEPOSIT" //这里可以是整数，或者表达式
    },
    "chain_spec": {
      "adminKey": "root.clone()"
    },
    "rpc_mod": false
  },
  "pallet_evm_utils": {
    "index": 26,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_pot": {
    "index": 27,
    "optional": false,
    "parameter": {
      "PotNames": ["system", "treasury", "maintenance"]
    },
    "chain_spec": {},
    "rpc_mod": true
  },
  "pallet_assurance": {
    "index": 28,
    "optional": false,
    "parameter": {
      "SystemPotName": "system",
      "DefaultBidThreshold": 8
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_utility": {
    "index": 29,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_liquidation": {
    "index": 30,
    "optional": false,
    "parameter": {
      "SystemRatio": 20,
      "TreasuryRatio": 33,
      "ProfitDistributionCycle": 10,
      "ExistDeposit": "EXISTENTIAL_DEPOSIT",
      "MinLiquidationThreshold": "MILLIUNIT * 20",
      "SystemAccountName": "system",
      "TreasuryAccountName": "treasury",
      "OperationAccountName": "maintenance"
    },
    "chain_spec": {
      "adminKey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
      "systemRatio": "20_000_0000", //这里是可以是整数，需要乘以10的7次方，比方20%就是20_000_0000,不分配利润则填写0
      "treasuryRatio": "33_000_0000",//这里是可以是整数，需要乘以10的7次方，不分配利润则填写0
      "operationRatios": [
        {"AccountId": "5GP7etLvS2VLLfUar7Q2TkQkaxHweYnDvrhh3s5hhf8eorPW", "ratio": "15_000_0000"}, //这里是ratio可以是整数，需要乘以10的7次方，不分配利润则填写0
        {"AccountId": "5CFuj7WxZAyinLxoqAJ8NH4yEEVXUUSHi9LRhodC3HyzHvN4", "ratio": "10_000_0000"} //这里是ratio可以是整数，需要乘以10的7次方，不分配利润则填写0
      ],
      "collatorRatio": "22_000_0000", //这里是ratio可以是整数，需要乘以10的7次方，不分配利润则填写0
      "minLiquidationThreshold": "20_000_000_000_000_000u128",
      "profitDistributionCycle": 10
    },
    "rpc_mod": false
  },
  "pallet_preimage": {
    "index": 31,
    "optional": false,
    "parameter": {
      "PreimageBaseDeposit": "deposit(2, 64)",
      "PreimageByteDeposit": "deposit(0, 1)",
      "PreimageHoldReason": "Preimage"
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_scheduler": {
    "index": 32,
    "optional": false,
    "parameter": {
      "MaximumSchedulerWeight": 80,
      "MaxScheduledPerBlock": 50,
      "NoPreimagePostponement": 10
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_insecure_randomness_collective_flip": {
    "index": 33,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_move": {
    "index": 34,
    "optional": false,
    "parameter": {
      "MultisigReqExpireTime": 50400,
      "MaxScriptSigners": 8
    },
    "chain_spec": {},
    "rpc_mod": true
  },
  "pallet_multisig": {
    "index": 35,
    "optional": false,
    "parameter": {
      "DepositBase": "228_000_000_000_000",
      "DepositFactor": "32_000_000_000_000",
      "MaxSignatories": 20
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_proxy": {
    "index": 36,
    "optional": false,
    "parameter": {
      "ProxyDepositBase": "160_000_000_000_000",
      "ProxyDepositFactor": "33_000_000_000_000",
      "MaxProxies": 100,
      "MaxPending": 1000,
      "AnnouncementDepositBase": "16_000_000_000_000",
      "AnnouncementDepositFactor": "64_000_000_000_000"
    },
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_conviction_voting": {
    "index": 37,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_referenda": {
    "index": 38,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_ranked_collective": {
    "index": 39,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_referenda_instance2": {
    "index": 40,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_custom_origins": {
    "index": 41,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_whitelist": {
    "index": 42,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  "pallet_xcm": {
    "index": 43,
    "optional": false,
    "parameter": {},
    "chain_spec": {
      "safeXcmVersion": "SAFE_XCM_VERSION"
    },
    "rpc_mod": false
  },
  "pallet_contracts": {
    "index": 44,
    "optional": false,
    "parameter": {},
    "chain_spec": {},
    "rpc_mod": false
  },
  //runtime_constant如果不写，会用默认值兼容处理
  "runtime_constant": {
    "BLOCK_GAS_LIMIT": "75_000_000",
    "MAX_POV_SIZE": "5 * 1024 * 1024"
  },
  "chain_spec_dev_constant": {
    //chain_spec里面的所有字段是必须填写的
    "tokenSymbol": "DOT", //如果是用DOT作为gas费，则传入DOT，不传入则默认为`DOT`
    "tokenDecimals": 18, //这里必须是整数类型
    "ss58Format": 42,
    "relay_chain": "rococo-local",
    "para_id": 2000,
    "name": "Development",
    "id": "dev",
    //collators里面必须填入地址，至少2个地址，保证parachain能够正常出块
    "collators": {
      "accountIdFromAddress": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y"],
      "collatorKeysFromAddress": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y"]
    },
    //endowedAccounts表示预添加地址，这里会结合`pallet_balances`里面的`chain_spec`里面的`endowed_accounts_supply`给地址添加初始账户资产
    "endowedAccountsFromAddress": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty", "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y", "5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy", "5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw", "5CiPPseXPECbkjWCa6MnjNokrgYjMqmKndv2rSnekmSK2DjL", "5GNJqTPyNqANBkUVMN1LPPrxXnFouWXoe2wNSmmEoLctxiZY", "5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK1iQ7qUsSWFc"],
    //这里是root账户地址
    "rootAccountFromAddress": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
  },
  //chain_spec_local_testnet_constant 格式与上面的chain_spec_dev_constant格式一致，后续版本优化，考虑将多个chain_spec_constant合并成一个
  "chain_spec_local_testnet_constant": {
    "tokenSymbol": "DOT",
    "tokenDecimals": 18,
    "ss58Format": 42,
    "relay_chain": "rococo-local",
    "para_id": 2000,
    "name": "Local Testnet",
    "id": "local_testnet",
    "collators": {
      "accountIdFromAddress": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y"],
      "collatorKeysFromAddress": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y"]
    },
    "endowedAccountsFromAddress": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty", "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y", "5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy", "5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw", "5CiPPseXPECbkjWCa6MnjNokrgYjMqmKndv2rSnekmSK2DjL", "5GNJqTPyNqANBkUVMN1LPPrxXnFouWXoe2wNSmmEoLctxiZY", "5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK1iQ7qUsSWFc"],
    "rootAccountFromAddress": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
  }
}
```
