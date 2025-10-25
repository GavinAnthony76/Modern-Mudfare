/**
 * UI Manager - Handles user interface updates and interactions
 */

class UIManager {
    constructor(game) {
        this.game = game;
        this.textOutput = document.getElementById('text-content');
        this.commandInput = document.getElementById('command-input');
        this.maxTextLines = 100;

        this.notifications = [];
        this.currentPanel = 'inventory';
    }

    addTextOutput(text, className = '') {
        if (!this.textOutput) return;

        const p = document.createElement('p');
        p.textContent = text;
        if (className) {
            p.className = className;
        }

        this.textOutput.appendChild(p);

        // Auto-scroll to bottom
        const container = document.getElementById('text-output');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }

        // Limit number of lines
        const lines = this.textOutput.getElementsByTagName('p');
        if (lines.length > this.maxTextLines) {
            this.textOutput.removeChild(lines[0]);
        }
    }

    clearTextOutput() {
        if (this.textOutput) {
            this.textOutput.innerHTML = '';
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--panel-bg);
            border: 2px solid var(--border-color);
            border-radius: 4px;
            color: var(--text-primary);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;

        if (type === 'success') {
            notification.style.borderColor = 'var(--success-color)';
            notification.style.color = 'var(--success-color)';
        } else if (type === 'warning') {
            notification.style.borderColor = 'var(--warning-color)';
            notification.style.color = 'var(--warning-color)';
        }

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    switchPanel(panelName) {
        // Update tabs
        document.querySelectorAll('.panel-tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.panel === panelName) {
                tab.classList.add('active');
            }
        });

        // Update panels
        document.querySelectorAll('.panel').forEach(panel => {
            panel.classList.remove('active');
        });

        const targetPanel = document.getElementById(`panel-${panelName}`);
        if (targetPanel) {
            targetPanel.classList.add('active');
            this.currentPanel = panelName;
        }
    }

    updateCharacterStats(stats) {
        // Update health
        const healthFill = document.querySelector('.health-fill');
        const healthValue = document.querySelector('.stat.health .stat-value');
        if (healthFill && healthValue && stats.health !== undefined) {
            const healthPercent = (stats.health / stats.maxHealth) * 100;
            healthFill.style.width = `${healthPercent}%`;
            healthValue.textContent = `${stats.health}/${stats.maxHealth}`;
        }

        // Update faith/mana
        const faithFill = document.querySelector('.faith-fill');
        const faithValue = document.querySelector('.stat.faith .stat-value');
        if (faithFill && faithValue && stats.faith !== undefined) {
            const faithPercent = (stats.faith / stats.maxFaith) * 100;
            faithFill.style.width = `${faithPercent}%`;
            faithValue.textContent = `${stats.faith}/${stats.maxFaith}`;
        }

        // Update character name and level
        const charName = document.getElementById('char-name-display');
        const charLevel = document.getElementById('char-level');
        if (charName && stats.name) {
            charName.textContent = stats.name;
        }
        if (charLevel && stats.level) {
            charLevel.textContent = `Level ${stats.level}`;
        }
    }

    updateInventory(items) {
        const inventoryGrid = document.querySelector('.inventory-grid');
        if (!inventoryGrid) return;

        // Clear existing items
        inventoryGrid.innerHTML = '';

        // Add items
        items.forEach(item => {
            const slot = document.createElement('div');
            slot.className = 'inventory-slot';
            slot.innerHTML = `
                <div class="item-icon">${item.icon || '?'}</div>
                <div class="item-name">${item.name}</div>
            `;
            slot.addEventListener('click', () => this.onInventoryItemClick(item));
            inventoryGrid.appendChild(slot);
        });

        // Add empty slots
        const emptySlots = Math.max(0, 12 - items.length);
        for (let i = 0; i < emptySlots; i++) {
            const slot = document.createElement('div');
            slot.className = 'inventory-slot empty';
            inventoryGrid.appendChild(slot);
        }
    }

    onInventoryItemClick(item) {
        console.log('Item clicked:', item);
        this.showNotification(`Selected: ${item.name}`, 'info');
    }

    updateQuests(quests) {
        const questList = document.querySelector('.quest-list');
        if (!questList) return;

        if (quests.length === 0) {
            questList.innerHTML = '<p class="empty-message">No active quests</p>';
            return;
        }

        questList.innerHTML = '';
        quests.forEach(quest => {
            const questItem = document.createElement('div');
            questItem.className = 'quest-item';
            questItem.innerHTML = `
                <h4>${quest.name}</h4>
                <p>${quest.description}</p>
                <div class="quest-progress">${quest.progress}/${quest.total}</div>
            `;
            questList.appendChild(questItem);
        });
    }

    toggleInventory() {
        this.switchPanel('inventory');
    }

    toggleQuests() {
        this.switchPanel('quests');
    }

    toggleMap() {
        this.switchPanel('map');
    }

    toggleSettings() {
        // TODO: Implement settings modal
        this.showNotification('Settings coming soon!', 'info');
    }

    focusCommandInput() {
        if (this.commandInput) {
            this.commandInput.focus();
        }
    }

    getCommandHistory() {
        const history = localStorage.getItem('commandHistory');
        return history ? JSON.parse(history) : [];
    }

    addToCommandHistory(command) {
        const history = this.getCommandHistory();
        history.push(command);

        // Keep only last 50 commands
        if (history.length > 50) {
            history.shift();
        }

        localStorage.setItem('commandHistory', JSON.stringify(history));
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
