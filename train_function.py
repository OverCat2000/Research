import torch
import torch.nn as nn
from tqdm.auto import tqdm
from timeit import default_timer as timer



if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f'There are {torch.cuda.device_count()} GPU(s) available.')
    print('Device name:', torch.cuda.get_device_name(0))

else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")


def train_step(model: torch.nn.Module,
               dataloader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
               optimizer: torch.optim.Optimizer):
    # Put model in train mode
    model.train()

    # Setup train loss and train accuracy values
    train_loss, train_acc = 0, 0

    # Loop through data loader data batches
    for batch, (X, y) in enumerate(dataloader):
        # 1. Forward pass
        X = X.to(device)
        y = y.to(device)

        # print(X.shape)
        y_pred = model(X)

        # print(y_pred)
        # print()
        # print(y)

        # 2. Calculate  and accumulate loss
        loss = loss_fn(y_pred.squeeze(1), y)
        train_loss += loss.item()

        # 3. Optimizer zero grad
        optimizer.zero_grad()

        # 4. Loss backward
        loss.backward()

        # 5. Optimizer step
        optimizer.step()

        # Calculate and accumulate accuracy metric across all batches
        train_acc += accuracy_fn(y_pred, y)

    # Adjust metrics to get average loss and accuracy per batch
    train_loss = train_loss / len(dataloader)
    train_acc = train_acc / len(dataloader)
    return train_loss, train_acc

def test_step(model: torch.nn.Module,
              dataloader: torch.utils.data.DataLoader,
              loss_fn: torch.nn.Module):
    # Put model in eval mode
    model.eval()

    # Setup test loss and test accuracy values
    test_loss, test_acc = 0, 0

    # Turn on inference context manager
    with torch.inference_mode():
        # Loop through DataLoader batches
        for batch, (X, y) in enumerate(dataloader):
            X = X.to(device)
            y = y.to(device)
            # 1. Forward pass
            test_pred_logits = model(X)

            # 2. Calculate and accumulate loss
            loss = loss_fn(test_pred_logits.squeeze(1), y)
            test_loss += loss.item()

            # Calculate and accumulate accuracy
            test_acc += accuracy_fn(test_pred_logits, y)

    # Adjust metrics to get average loss and accuracy per batch
    test_loss = test_loss / len(dataloader)
    test_acc = test_acc / len(dataloader)
    return test_loss, test_acc

import torch
from tqdm import tqdm
import copy

def train(model: torch.nn.Module,
          train_dataloader: torch.utils.data.DataLoader,
          test_dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module,
          epochs: int = 5):

    # Create empty results dictionary
    results = {
        "train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": []
    }

    # Track the best model state
    best_test_acc = 0.0
    best_model = copy.deepcopy(model)  # Create a separate best model instance

    try:
        # Loop through training and testing steps for a number of epochs
        for epoch in tqdm(range(epochs)):
            train_loss, train_acc = train_step(model=model,
                                               dataloader=train_dataloader,
                                               loss_fn=loss_fn,
                                               optimizer=optimizer)
            test_loss, test_acc = test_step(model=model,
                                            dataloader=test_dataloader,
                                            loss_fn=loss_fn)

            # Print epoch results
            print(
                f"Epoch: {epoch+1} | "
                f"train_loss: {train_loss:.4f} | "
                f"train_acc: {train_acc:.4f} | "
                f"test_loss: {test_loss:.4f} | "
                f"test_acc: {test_acc:.4f}"
            )

            # Update results dictionary
            results["train_loss"].append(train_loss)
            results["train_acc"].append(train_acc)
            results["test_loss"].append(test_loss)
            results["test_acc"].append(test_acc)

            # Save the best model based on test accuracy
            if test_acc > best_test_acc:
                best_test_acc = test_acc
                best_model = copy.deepcopy(model)  # Store a full copy of the model

    except KeyboardInterrupt:
        print("\nTraining interrupted. Returning results so far...")

    print(f"Best model test accuracy: {best_test_acc:.4f}")

    # Return results, trained model, and best model
    return results, model, best_model


def train_old(model: torch.nn.Module,
          train_dataloader: torch.utils.data.DataLoader,
          test_dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module,
          epochs: int = 5):

    # 2. Create empty results dictionary
    results = {"train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": []
    }

    try:
        # 3. Loop through training and testing steps for a number of epochs
        for epoch in tqdm(range(epochs)):
            train_loss, train_acc = train_step(model=model,
                                               dataloader=train_dataloader,
                                               loss_fn=loss_fn,
                                               optimizer=optimizer)
            test_loss, test_acc = test_step(model=model,
                dataloader=test_dataloader,
                loss_fn=loss_fn)

            # 4. Print out what's happening
            print(
                f"Epoch: {epoch+1} | "
                f"train_loss: {train_loss:.4f} | "
                f"train_acc: {train_acc:.4f} | "
                f"test_loss: {test_loss:.4f} | "
                f"test_acc: {test_acc:.4f}"
            )

            # 5. Update results dictionary
            results["train_loss"].append(train_loss)
            results["train_acc"].append(train_acc)
            results["test_loss"].append(test_loss)
            results["test_acc"].append(test_acc)

    except KeyboardInterrupt:
        print("\nTraining interrupted. Returning results so far...")

    # 6. Return the filled results at the end of the epochs or if interrupted
    return results


class BinaryAccuracy:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def __call__(self, logits, targets):
        # Apply sigmoid to logits to get probabilities
        probabilities = torch.sigmoid(logits).squeeze(dim=1)
        # Convert probabilities to binary predictions
        predictions = (probabilities >= self.threshold).float()
        # Compare predictions with targets and calculate accuracy
        correct = (predictions == targets).float().sum()
        accuracy = correct / targets.numel()
        return accuracy.item()

class MultiClassAccuracy:
    def __init__(self):
        pass

    def __call__(self, logits, targets):
        # Apply softmax to logits to get class probabilities (optional, for insight)
        # probabilities = torch.softmax(logits, dim=1)

        # Get the predicted class indices by applying argmax to logits
        predictions = torch.argmax(logits, dim=1)

        # Compare predictions with targets and calculate accuracy
        correct = (predictions == targets).float().sum()
        accuracy = correct / targets.numel()  # Total number of samples
        return accuracy.item()


accuracy_fn = MultiClassAccuracy()
