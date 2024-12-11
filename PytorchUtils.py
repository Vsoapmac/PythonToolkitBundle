"""
pytorch工具类, 用于简化pytorch模型的训练过程等
\n使用该模块, 请执行以下命令安装所需库
\n注意, 以下示例为cuda12.4的版本, 如果设备不为cuda12,4, 请进入https://pytorch.org/get-started/locally/ 并按照实际情况选择版本:
\npip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
\npip install progressbar
\npip install tensorboard
"""
import torch, os, time
from torch import nn, device
from torch.optim import Adam
from progress.bar import ChargingBar
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


def train_epoch(model: nn.Module, loader: DataLoader, criterion, optimizer: Adam, device: device) -> tuple:
    """训练模型, 这是一轮的训练过程

    Args:
        model (nn.Module): 模型
        loader (DataLoader): 数据加载器
        criterion (nn.Loss): 损失函数
        optimizer (torch.optim): 优化器
        device (torch.device): 设备(cpu、cuda等)

    Returns:
        float: 训练损失, 训练准确率
    """
    model.train() # 设置模型为训练模式
    total_perdict_count = 0  # 初始化总预测的数量为0
    correct_predict_count = 0  # 初始化正确预测的数量为0
    total_loss = 0.0  # 初始化总损失为0
    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)

        # 前向传播
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # 累加损失, 将损失值乘以批量大小。这样做的原因是为了在计算总损失时，考虑到每个批次中的样本数量。如果直接累加损失值，那么总损失会偏向于样本数量较大的批次。
        total_loss += loss.item() * inputs.size(0)
        
        # 计算准确率
        _, predicted = torch.max(outputs.data, 1) # 获取预测结果
        total_perdict_count += labels.size(0) # 计算总预测样本数量
        correct_predict_count += (predicted == labels).sum().item() # 计算预测正确的样本数量
        
    # 计算平均损失和准确率
    avg_loss = total_loss / len(loader.dataset)
    avg_accuracy = correct_predict_count / total_perdict_count if total_perdict_count != 0 else 0
    return avg_loss, avg_accuracy

def validate_epoch(model: nn.Module, loader: DataLoader, criterion, device: device) -> tuple:
    """验证模型, 这是一轮的验证过程

    Args:
        model (nn.Module): 模型
        loader (DataLoader): 数据加载器
        criterion (nn.Loss): 损失函数
        device (torch.device): 设备(cpu、cuda等)

    Returns:
        float: 验证损失, 验证准确率
    """
    model.eval() # 设置为评估模式, 禁用诸如批量归一化、Dropout等与训练相关的操作
    # 初始化损失和正确率变量
    running_loss = 0.0
    correct = 0
    total = 0
    # 使用torch.no_grad()上下文, 禁用梯度计算, 减少内存使用并提高计算速度，因为在评估过程中不需要计算梯度。
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs) # 预测结果
            # 计算损失
            loss = criterion(outputs, labels)
            running_loss += loss.item() * inputs.size(0)
            
            # 更新损失和正确率
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / len(loader.dataset) if len(loader.dataset) != 0 else 0 # 计算平均损失
    accuracy = correct / total if total != 0 else 0 # 计算准确率
    return epoch_loss, accuracy

def train(model: nn.Module, num_epochs: int, criterion, optimizer: Adam, device: device, 
         tran_loader: DataLoader, val_loader: DataLoader=None, is_validate: bool=True, 
         is_save_model: bool=False, save_model_dir: str=None, 
         is_log_tensorboard: bool=False, tensorboard_log_dir: str="./", tensorboard_log_comment: str="", 
         tensorboard_filename_suffix: str = "") -> tuple:
    """训练模型

    Args:
        model (nn.Module): 模型
        num_epoch (int): 训练轮数
        criterion (nn.Loss): 损失函数
        optimizer (torch.optim): 优化器
        device (device): 设备(cpu、cuda等)
        tran_loader (DataLoader): 训练数据加载器
        val_loader (DataLoader, optional): 验证数据加载器, 前提是is_validate参数设置为True. Defaults to None.
        is_validate (bool, optional): 是否验证模型. Defaults to True.
        is_save_model (bool, optional): 是否保存模型. Defaults to False.
        save_model_dir (str, optional): 保存模型文件夹路径. Defaults to None.
        is_log_tensorboard (bool, optional): 是否写入tensorboard. Defaults to False.
        tensorboard_log_dir (str, optional): TensorBoard logs输出路径, 如果is_log_tensorboard参数指定为True, 该参数不能为None. Defaults to "./".
        tensorboard_log_comment (str, optional): 不指定tensorboard_log_dir时, log的文件夹后缀. Defaults to "".
        tensorboard_filename_suffix (str, optional): event file文件名后缀. Defaults to "".

    Returns:
        tuple: 已训练好的模型, 最佳模型权重
    """
    if is_log_tensorboard:
        if tensorboard_log_dir is None:
            raise Exception("Please provide a directory for TensorBoard logs. Specify a valid directory using the 'tensorboard_log_dir' parameter.")
        writer = SummaryWriter(log_dir=tensorboard_log_dir, comment=tensorboard_log_comment, filename_suffix=tensorboard_filename_suffix)
    else:
        writer = None
    # 定义最佳准确度与最佳模型权重
    best_accuracy = 0.0
    best_model_weights = None
    model.to(device)
    
    # region =========================== 训练过程 ===========================
    progress_bar = ChargingBar("Training..", max=num_epochs)
    start_time = time.time()
    for epoch in range(num_epochs):
        progress_bar.next()
        epoch_start_time = time.time()
        
        # region ------------------------- 训练 -------------------------
        train_loss, train_accuracy = train_epoch(model, tran_loader, criterion, optimizer, device) # 训练
        # 统计训练时间
        train_time_spend = time.time() - epoch_start_time
        train_time_spend_result = f"{round(train_time_spend / 60, 3)} min" if 60 * 60 > train_time_spend > 60  \
                else f"{round(train_time_spend / 60 / 60, 3)} h" if train_time_spend > 60 * 60 \
                else f"{round(train_time_spend, 3)} s"
        # 写入到tensorboard
        if writer is not None:
            writer.add_scalar("Train Loss", train_loss, epoch)
            writer.add_scalar("Train Accuracy", train_accuracy, epoch)
        # endregion ------------------------- 训练 -------------------------
        
        # region ------------------------- 验证 -------------------------
        if is_validate:
            val_loss, val_accuracy = validate_epoch(model, val_loader, criterion, device) # 验证
            # 统计训练+验证的总时间
            train_val_time_spend = time.time() - epoch_start_time
            train_val_time_spend_result = f"{round(train_val_time_spend / 60, 3)} min" if 60 * 60 > train_val_time_spend > 60  \
                    else f"{round(train_val_time_spend / 60 / 60, 3)} h" if train_val_time_spend > 60 * 60 \
                    else f"{round(train_val_time_spend, 3)} s"
            print(f" Spend Time: {train_val_time_spend_result} Epoch {epoch+1}/{num_epochs}, " \
                  f"Train Loss: {round(train_loss, 4)}, Train Accuracy: {round(train_accuracy, 4)}, " \
                  f"Val Loss: {round(val_loss, 4)}, Val Accuracy: {round(val_accuracy, 4)}, ")
            # 写入到tensorboard
            if writer is not None:
                writer.add_scalar("Val Loss", val_loss, epoch)
                writer.add_scalar("Val Accuracy", val_accuracy, epoch)
                
            # 保存最佳模型权重与准确率
            if val_accuracy > best_accuracy:
                best_accuracy = val_accuracy
                best_model_weights = model.state_dict()
        else:
            print(f" Spend Time: {train_time_spend_result} Epoch {epoch+1}/{num_epochs}, Train Loss: {round(train_loss, 4)}, " \
                f"Train Accuracy: {round(train_accuracy, 4)}")
        # endregion ------------------------- 验证 -------------------------
        
    # endregion =========================== 训练过程 ===========================
    
    # region =========================== 统计总耗时 ===========================
    progress_bar.finish()
    total_time_spend = time.time() - start_time
    total_time_spend_result = f"{round(total_time_spend / 60, 3)} min" if 60 * 60 > total_time_spend > 60  \
            else f"{round(total_time_spend / 60 / 60, 3)} h" if total_time_spend > 60 * 60 \
            else f"{round(total_time_spend, 3)} s"
    print(f"Training finished, total spend time: {total_time_spend_result}")
    # endregion =========================== 统计总耗时 ===========================
    
    # region =========================== 保存训练结果 ===========================
    if is_save_model:
        if is_validate:
            # 保存模型与最佳模型
            torch.save(best_model_weights, os.path.join(save_model_dir, "best_model.pth"))
            print(f"Best Validation Accuracy: {round(best_accuracy, 4)}")
        torch.save(model.state_dict(), os.path.join(save_model_dir, "model.pth"))
        print(f"saved model in: {save_model_dir}, the model name is: model.pth {'and best_model.pth' if is_validate else ''}")
    # 关闭tensorboard
    if writer is not None:
        writer.close()
    # endregion =========================== 保存训练结果 ===========================
    return model, best_model_weights

def load_model(model: nn.Module, model_weight_path: str, device: device) -> nn.Module:
    """加载模型

    Args:
        model (nn.Module): 模型, 一般是模型结构
        model_weight_path (str): 已训练的模型权重
        device (device): 设备(cpu、cuda等)

    Returns:
        nn.Module: 加载后的模型
    """
    loaded_model = model.load_state_dict(torch.load(model_weight_path)) # 加载模型权重
    loaded_model.to(device) # 将模型移动到指定设备
    return loaded_model
